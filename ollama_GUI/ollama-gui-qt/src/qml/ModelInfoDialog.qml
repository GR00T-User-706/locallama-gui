import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Dialog {
    id: infoDialog
    property string modelName: ""
    title: "Model Info – " + modelName
    standardButtons: Dialog.Ok
    width: 500
    height: 450
    modal: true
    onModelNameChanged: {
        if (modelName !== "") {
            backend.showModelInfo(modelName)
        }
    }
    onOpened: {
        if (modelName !== "") {
            backend.showModelInfo(modelName)
        }
    }

    ColumnLayout {
        anchors.fill: parent
        BusyIndicator {
            visible: backend.modelInfoLoading
            running: backend.modelInfoLoading
            Layout.alignment: Qt.AlignCenter
        }
        Label {
            text: "Unable to load model info."
            visible: !backend.modelInfoLoading && backend.modelInfoJson === ""
        }
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: backend.modelInfoJson !== ""
            TextArea {
                id: infoText
                readOnly: true
                wrapMode: Text.WordWrap
                font.family: "monospace"
                text: {
                    var jsonString = backend.modelInfoJson
                    if (jsonString === "") return ""
                    var obj = JSON.parse(jsonString)
                    var out = ""
                    // Basic info
                    if (obj.modelfile) {
                        out += "=== Basic Information ===\n"
                        // Try to parse some fields from modelfile? Not robust.
                        out += "Model file present (see advanced)\n"
                    }
                    out += "Modified: " + (obj.modified_at || "N/A") + "\n"
                    out += "Size: " + (obj.size || "N/A") + "\n"
                    out += "Digest: " + (obj.digest || "N/A") + "\n"
                    // Details
                    if (obj.details) {
                        var det = obj.details
                        out += "\n=== Technical Details ===\n"
                        out += "Family: " + (det.family || "N/A") + "\n"
                        out += "Parameter size: " + (det.parameter_size || "N/A") + "\n"
                        out += "Quantization: " + (det.quantization_level || "N/A") + "\n"
                        out += "Format: " + (det.format || "N/A") + "\n"
                    }
                    if (obj.modelfile) {
                        out += "\n=== Advanced (Modelfile) ===\n"
                        var modelfile = obj.modelfile
                        // Show first 30 lines
                        var lines = modelfile.split("\n")
                        var count = Math.min(30, lines.length)
                        for (var i = 0; i < count; ++i)
                            out += lines[i] + "\n"
                        if (lines.length > 30)
                            out += "...\n"
                    }
                    return out
                }
            }
        }
    }
}