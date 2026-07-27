# difflogic

微分可能論理ゲートネットワーク（Differentiable Logic Gate Network）の最小実装。
学習後に`argmax`でゲートを確定させるとそのまま組み合わせ回路になるので、Verilogに書き出して論理シミュレータで検証できるところまで実装する。

```bash
difflogic_project/
├── difflogic/
│   ├── gates.py      16種のブール関数と実数緩和（多重線形拡張）
│   ├── layers.py     LogicLayer / GroupSum
│   ├── models.py     LogicNet と診断メソッド
│   ├── tasks.py      学習タスク（全数列挙できる小問題）
│   ├── train.py      学習ループと評価
│   └── export.py     ネットリスト抽出・枝刈り・Verilog/TB 生成
├── tests/
│   └── test_gates.py 緩和が真理値表と一致することの検証
├── run.py            CLI エントリポイント
└── README.md
```

依存はPyTorchのみ。回路を検証するならIcarus Verilogを使用する。

```bash
brew install icarus-verilog
```

## 実行方法

```bash
python run.py # 比較器タスク（動作確認用）
python run.py --task parity # 学習できない例を観察する
python run.py --depth 10 # 勾配消失を観察する
python run.py --depth 10 --residual-init 3.0 # 残差初期化で救う
```

出力された回路を検証する。

```bash
cd out && iverilog -o tb logicnet.v tb.v && ./tb
# -> OK: 全256通りで Python の予測と一致
```

テストを実行する。

```bash
python om pytest tests -q
```

## 各モジュール

### gates.py

ゲート番号`i`の下位4bitがそのまま真理値表になっている。

```bash
i = T00*8 + T01*4 + T10*2 + T11*1
i=1 = 0b0001 -> AND
i=6 = 0b0110 -> XOR
i=14 = 0b1110 -> NAND
```

よって16本の式を逐次列挙する必要はなく、多重線形拡張を行う。

```bash
f_T(a, b) = T00(1-a)(1-b) + T01(1-a)b + T10*a(1-b) + T11*ab
```

上式に真理値表を代入すればすべて出力される。実装は基底の4項と真理値表`[16, 4]`の行列積で1度に求められる。

`gate_deps(i)`は「そのゲートが a/b に実際に依存するか」を真理値表から判定する。定数ゲートは両方に依存せず、恒等ゲート`A`はaのみである（最適化に使用）。

### layers.py

配線`idx_a, idx_b`はランダム固定で学習しない。学習するのは`w: [out_dim, 16]`のみである（ノードあたり16パラメータ）。
`residual_init`は恒等ゲートに初期バイアスを乗せる。恒等ゲートは`df/da = 1`で信号を減衰させないので、深い層でも勾配が残る。

### export.py

出力から逆向きに辿って到達可能なノードだけを残す。ランダム配線なので使えないノードは必ず出る。
学習時のノード数は回路規模の過大評価になるため注意する。

## 実測

## Next-ToDo

- [ ] 2値化 MNIST で実タスクに乗せる
- [ ] Yosys で合成して LUT 数を実測する
- [ ] Straight-Throught Estimator で discretization gap を潰す
- [ ] k入力 LUT への一般化（FPGA の LUT6 に直接対応）
- [ ] 配線の学習（現状の最大の弱点）
