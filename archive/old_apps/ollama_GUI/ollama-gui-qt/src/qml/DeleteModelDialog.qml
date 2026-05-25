import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Dialog {
    id: deleteDialog
    property string modelName: ""
    title: "Delete Model"
    standardButtons: Dialog.NoButton
    modal: true
    ColumnLayout {
        spacing: 10
        Label {
            text: "Are you sure you want to permanently delete '" + modelName + "'?"
            wrapMode: Text.WordWrap
            Layout.maximumWidth: 300
        }
        RowLayout {
            Layout.alignment: Qt.AlignRight
            Button {
                text: "Cancel"
                onClicked: deleteDialog.reject()
            }
            Button {
                text: "Delete"
                highlighted: true
                onClicked: {
                    if (modelName !== "") {
                        backend.removeModel(modelName)
                    }
                    deleteDialog.accept()
                }
            }
        }
    }
}