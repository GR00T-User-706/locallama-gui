import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Dialog {
    id: pullProgressDialog
    title: "Pull Progress"
    standardButtons: Dialog.NoButton
    modal: false
    closePolicy: Popup.NoAutoClose
    property bool active: backend.pullInProgress

    onActiveChanged: {
        if (active) open()
        else close()
    }

    ColumnLayout {
        width: 400
        Label { text: "Pulling model..." }
        Label { text: backend.pullProgressText }
        ProgressBar {
            indeterminate: backend.pullProgressTotal <= 0
            from: 0
            to: backend.pullProgressTotal > 0 ? backend.pullProgressTotal : 1
            value: backend.pullProgressCompleted
            Layout.fillWidth: true
            visible: backend.pullProgressTotal > 0
        }
        RowLayout {
            Button {
                text: "Cancel"
                onClicked: {
                    backend.cancelCurrentOperation()
                    pullProgressDialog.close()
                }
            }
        }
    }
}