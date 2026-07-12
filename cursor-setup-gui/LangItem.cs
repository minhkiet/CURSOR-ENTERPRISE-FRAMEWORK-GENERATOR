namespace CursorSetup
{
    internal class LangItem
    {
        public string Code { get; }
        public LangItem(string code, string display) { Code = code; Display = display; }
        public string Display { get; }
        public override string ToString() { return Display; }
    }
}
