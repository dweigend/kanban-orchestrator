# ⚙️ Settings Components

> Modular settings panel components for the Kanban Orchestrator app

## 📋 Contents

| File | Description |
|------|-------------|
| `SettingsPanel.svelte` | Container/Orchestrator for all settings sections |
| `SettingsAccordionItem.svelte` | Reusable accordion container with icon |
| `SettingToggle.svelte` | Toggle switch with label and description |
| `SettingSlider.svelte` | Slider with label and value display |
| `SettingSelect.svelte` | Dropdown select with label |

## 🏗️ Architecture

```
SettingsPanel (Container)
├── SettingsAccordionItem (Editor)
│   ├── SettingSelect (Font Family)
│   └── SettingSlider (Font Size)
├── SettingsAccordionItem (Git)
│   └── SettingToggle (Auto Checkpoint)
├── SettingsAccordionItem (Agent)
│   ├── SettingSelect (Model)
│   └── SettingSlider (Max Turns)
├── SettingsAccordionItem (Notifications)
│   └── SettingToggle
└── SettingsAccordionItem (Privacy)
    └── SettingToggle (Analytics)
```

## 🎯 Design Principles

1. **Props over local state**: No `state_referenced_locally` warnings
2. **Single responsibility**: Each component has one job
3. **Reusable**: Toggle, Slider, Select can be used anywhere
4. **Consistent styles**: All components use the same CSS variables

## 🔧 Usage

```svelte
<script>
  import SettingsPanel from '$lib/components/settings/SettingsPanel.svelte';
</script>

<SettingsPanel />
```
