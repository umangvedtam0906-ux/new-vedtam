Set objFSO = CreateObject("Scripting.FileSystemObject")
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

Set objShell = CreateObject("WScript.Shell")
objShell.CurrentDirectory = strPath
' Run the Node.js updater completely hidden (0 = no window)
objShell.Run "cmd /c node update-cert-data.mjs >> cert-update-log.txt 2>&1", 0, False
