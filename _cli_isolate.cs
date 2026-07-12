using System;
using System.IO;
using System.IO.Compression;
using System.Threading.Tasks;

class TestCli {
    [STAThread]
    static int Main(string[] args) {
        try {
            File.WriteAllText("test-cli.log", $"args: {string.Join(",", args)}\ncwd: {Environment.CurrentDirectory}\n");
            string zipPath = @"D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR\_cli_test.zip";
            File.AppendAllText("test-cli.log", $"zip exists: {File.Exists(zipPath)}\n");
            using (var archive = ZipFile.OpenRead(zipPath)) {
                File.AppendAllText("test-cli.log", $"entries: {archive.Entries.Count}\n");
            }
            return 0;
        } catch (Exception ex) {
            File.AppendAllText("test-cli.log", $"FAIL: {ex.GetType().Name}: {ex.Message}\n{ex.StackTrace}\n");
            return 1;
        }
    }
}