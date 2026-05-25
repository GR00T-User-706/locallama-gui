import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Dialog {
    id: createDialog
    title: "Create Model"
    standardButtons: Dialog.NoButton
    modal: true
    ColumnLayout {
        width: 450
        Label { text: "Model name:" }
        TextField { id: createModelName }
        Label { text: "Modelfile:" }
        ScrollView {
            Layout.fillWidth: true
            Layout.preferredHeight: 200
            TextArea {
                id: modelfileEditor
                wrapMode: TextArea.Wrap
                font.family: "monospace"
                text: "FROM " + backend.currentModel + "\n"
            }
        }
        Button { text: "Load from file..."; onClicked: createFileDialog.open() }
        BusyIndicator {
            running: backend.createInProgress
            visible: backend.createInProgress
        }
        Label {
            visible: backend.createInProgress
            text: backend.createProgressText
        }
        RowLayout {
            Button { text: "Cancel"; onClicked: createDialog.reject() }
            Button {
                text: "Create"
                enabled: createModelName.text.trim() !== "" && !backend.createInProgress
                onClicked: {
                    backend.createModel(createModelName.text.trim(), modelfileEditor.text)
                    if (!backend.createInProgress) createDialog.accept()
                }
            }
        }
    }
    FileDialog {
        id: createFileDialog
        title: "Load Modelfile"
        nameFilters: ["Text files (*.txt)", "All files (*)"]
        onAccepted: {
            var path = fileUrl.toString().replace("file://", "")
            // Load via network or file? We'll just use QML's FileApi? Better to call C++.
            backend.loadModelfileFromFile(fileUrl) // need to implement in Backend
        }
    }
}