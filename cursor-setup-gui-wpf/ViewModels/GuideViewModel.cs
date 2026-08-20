#nullable enable
using CursorSetupWpf.Services;

namespace CursorSetupWpf.ViewModels
{
    /// <summary>
    /// ViewModel for GuideView - provides localized strings for the user guide content.
    /// Uses LocalizationService.T() for runtime language switching.
    /// </summary>
    public class GuideViewModel : ViewModelBase
    {
        public GuideViewModel()
        {
            // Subscribe to culture changes to refresh all bindings
            LocalizationService.CultureChanged += () =>
            {
                // Fire PropertyChanged for all localized properties
                OnPropertyChanged(string.Empty);
            };
        }

        // Welcome Banner
        public string WelcomeTitle => LocalizationService.T("guide.welcome");
        public string WelcomeSubtitle => LocalizationService.T("guide.intro");
        public string WelcomeIcon => "\uE8B7";

        // Steps Section Title
        public string StepsTitle => LocalizationService.T("guide.steps_title");

        // Step 1
        public string Step1Title => LocalizationService.T("guide.step1_title");
        public string Step1Description => LocalizationService.T("guide.step1_desc");
        public string Step1Tip => LocalizationService.T("guide.step1_tip");

        // Step 2
        public string Step2Title => LocalizationService.T("guide.step2_title");
        public string Step2Description => LocalizationService.T("guide.step2_desc");
        public string Step2Item1 => LocalizationService.T("guide.step2_item1");
        public string Step2Item2 => LocalizationService.T("guide.step2_item2");
        public string Step2Item3 => LocalizationService.T("guide.step2_item3");
        public string Step2Item4 => LocalizationService.T("guide.step2_item4");
        public string Step2Item5 => LocalizationService.T("guide.step2_item5");
        public string Step2Item6 => LocalizationService.T("guide.step2_item6");

        // Step 3
        public string Step3Title => LocalizationService.T("guide.step3_title");
        public string Step3Description => LocalizationService.T("guide.step3_desc");

        // Step 4
        public string Step4Title => LocalizationService.T("guide.step4_title");
        public string Step4Description => LocalizationService.T("guide.step4_desc");

        // Step 5 (Final)
        public string Step5Title => LocalizationService.T("guide.step5_title");
        public string Step5Description => LocalizationService.T("guide.step5_desc");

        // About Section
        public string AboutTitle => LocalizationService.T("guide.about_title");
        public string AboutIntro => LocalizationService.T("guide.about_intro");
        public string ArchitectureTitle => LocalizationService.T("guide.architecture_title");
        public string ArchitectureDesc => LocalizationService.T("guide.architecture_desc");
        public string AiAgentTitle => LocalizationService.T("guide.ai_agent_title");
        public string AiAgentDesc => LocalizationService.T("guide.ai_agent_desc");
        public string DevToolsTitle => LocalizationService.T("guide.devtools_title");
        public string DevToolsDesc => LocalizationService.T("guide.devtools_desc");
        public string DeployOpsTitle => LocalizationService.T("guide.deploy_ops_title");
        public string DeployOpsDesc => LocalizationService.T("guide.deploy_ops_desc");

        // Info icon
        public string InfoIcon => "\uE946";
    }
}
