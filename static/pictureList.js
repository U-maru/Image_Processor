
// 「問題へ進む」ボタンを押した時の処理
const startQuizButton = document.querySelector('.startQuiz')
startQuizButton.addEventListener("click", (event) => {
    // 現在動作中のクリックイベント以外のボタンイベントをキャンセル（データの送信自体もキャンセルされる）
    event.preventDefault()

    selectMode = document.querySelector('.select-mode').mode
    let mode = "";

    for (let i = 0; i < selectMode.length; i++) {
        if (selectMode[i].checked) {
            mode = selectMode[i].value;
            break;
        }
    }
    console.log("選択されたモード : ", mode)


    selectImage = document.querySelector('.select-img').img
    let image = "";
    console.log(selectImage.length)

    if (selectImage.length == undefined && document.getElementById("0").checked) {
        image = document.getElementById("0").value
    }

    for (let j = 0; j < selectImage.length; j++) {
        if (selectImage[j].checked) {
            image = selectImage[j].value;
            console.log(j, "番目の画像を選択しました！")
            break;
        }
    }
    console.log("選択された画像 : ", image)

    if (image != "") {
        // 登録するデータを収集
        const formData = new FormData()
        formData.append("mode", mode)
        formData.append("image", image)

        console.log("送信データ:formData", ...formData)

        // データ登録のWeb APIを/add_ToDoをPOSTメソッドで呼び出す
        fetch("/setData", {
            method: 'POST',
            body: formData, // 登録するデータ(FormData形式)
        }).then((response) => {
            console.log("送信されたデータ", response)

            location.href = "/test"
        })
    } else {
        alert("画像を選択して下さい")
    }
})