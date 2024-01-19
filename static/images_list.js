// 「削除」ボタン要素をすべて取得
var delete_buttons = document.querySelectorAll('.delete');
// ボタンごとにイベントリスナーを追加
delete_buttons.forEach(function(btn_delete) {
    btn_delete.addEventListener('click', (event) => {
        // 現在動作中のクリックイベント以外のボタンイベントをキャンセル（データの送信自体もキャンセルされる）
        event.preventDefault()

        // 押されたボタンのidを取得
        const btn_id = btn_delete.id
        
        // 登録するデータを収集
        const formData = new FormData()
        formData.append("img_name", btn_id)

        console.log("JavaScript > Python : ", ...formData)

        // データ登録のWeb APIを/remove_ToDoをPOSTメソッドで呼び出す
        fetch("/delete_one", {
            method: 'POST',
            body: formData,
        }).then((response) => {
            console.log("Python > JavaScript : ", response)

            // ページの再読み込み
            location.reload()
        })
    });
});