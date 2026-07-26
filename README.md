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

## 各モジュール

### gates.py

### layers.py

### export.py

## 実測

## Next-ToDo

- [ ] 2値化 MNIST で実タスクに乗せる
- [ ] Yosys で合成して LUT 数を実測する
- [ ] Straight-Throught Estimator で discretization gap を潰す
- [ ] k入力 LUT への一般化（FPGA の LUT6 に直接対応）
- [ ] 配線の学習（現状の最大の弱点）
# difflogic
