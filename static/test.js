
const submitAnswerButton = document.getElementById("submit-answer")
submitAnswerButton.addEventListener("click", (event) => {
    // 現在動作中のクリックイベント以外のボタンイベントをキャンセル（データの送信自体もキャンセルされる）
    event.preventDefault()

    // 答えを取得
    answer = document.querySelector(".changedImage").id
    console.log("答え -> ", answer)

    // 選択された選択肢がどれか取得
    selectAnswer = document.querySelector('.select-answer').answer
    let yourAnswer = "";

    // 選択された選択肢がどれか取得
    for (let i = 0; i < selectAnswer.length; i++) {
        if (selectAnswer[i].checked) {
            // 選択された回答を代入
            yourAnswer = selectAnswer[i].value;
            break;
        }
    }
    console.log("あなたの回答 -> ", yourAnswer)

    // 正誤判定をおこない、結果に合わせたアラートを表示
    if (answer == yourAnswer) {
        alert("正解です！！")
    } else {
        alert("不正解です...")
    }
})