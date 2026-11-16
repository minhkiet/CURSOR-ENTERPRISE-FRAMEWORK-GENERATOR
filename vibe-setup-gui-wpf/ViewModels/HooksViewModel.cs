#nullable enable
using CursorSetupWpf.Services;

namespace CursorSetupWpf.ViewModels
{
    /// <summary>
    /// ViewModel for HooksView - provides localized strings for the hooks configuration page.
    /// Uses LocalizationService.T() for runtime language switching.
    /// </summary>
    public class HooksViewModel : ViewModelBase
    {
        public HooksViewModel()
        {
            LocalizationService.CultureChanged += () =>
            {
                OnPropertyChanged(string.Empty);
            };
        }

        // Page Header
        public string PageTitle => LocalizationService.T("hooks.page_title");
        public string PageDescription => LocalizationService.T("hooks.page_desc");

        // Pre-scan Hook
        public string PrescanTitle => LocalizationService.T("hooks.prescan_title");
        public string PrescanDescription => LocalizationService.T("hooks.prescan_desc");
        public string PrescanScriptLabel => LocalizationService.T("hooks.prescan_script_label");

        // Post-install Hook
        public string PostinstallTitle => LocalizationService.T("hooks.postinstall_title");
        public string PostinstallDescription => LocalizationService.T("hooks.postinstall_desc");
        public string PostinstallScriptLabel => LocalizationService.T("hooks.postinstall_script_label");

        // About Section
        public string AboutTitle => LocalizationService.T("hooks.about_title");
        public string AboutDescription => LocalizationService.T("hooks.about_desc");
    }
}
