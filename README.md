# エアコンのコントロール
## 概要
[Loopでんきのでんき予報](https://looop-denki.com/home/denkiforecast/)からAPIを取得して、電気代が高い際にSwithBotを使用してエアコンの電源を切ります。

## 問題点
仮作成であり、暖房の温度23℃に必ずなるようにしています。

## やりたいこと
- 外気温を考慮したうえで、室温の温度を調整する
- 一日の総額の電気代を最小にしつつ、室温を一定にする
- on,offにしか対応していないため、「温度、風量」を調整する