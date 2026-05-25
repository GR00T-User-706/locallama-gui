import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Dialog {
    id: diagnosticsDialog
    title: "Diagnostics"
    standardButtons: Dialog.Ok
    modal: true
    ColumnLayout {
        Label { text: "Connection Test" }
        Button {
            text: "Test Connection"
            onClicked: backend.testConnection()
        }
        Label {
            text: "Result will appear in chat output."
            Layout.maximumWidth: 300
        }
    }
}