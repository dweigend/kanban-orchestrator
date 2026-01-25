# Settings Components

Modular settings panel components für die Kanban Orchestrator App.

## Komponenten

| Datei | Beschreibung |
|-------|--------------|
| `SettingsPanel.svelte` | Container/Orchestrator für alle Settings-Sections |
| `SettingsAccordionItem.svelte` | Wiederverwendbarer Accordion-Container mit Icon |
| `SettingToggle.svelte` | Toggle-Switch mit Label und Description |
| `SettingSlider.svelte` | Slider mit Label und Value-Anzeige |
| `SettingSelect.svelte` | Dropdown-Select mit Label |

## Architektur

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

## Design-Prinzipien

1. **Props statt lokaler State**: Keine `state_referenced_locally` Warnings
2. **Single Responsibility**: Jede Komponente hat eine Aufgabe
3. **Wiederverwendbar**: Toggle, Slider, Select können überall genutzt werden
4. **Konsistente Styles**: Alle Komponenten nutzen die gleichen CSS-Variablen

## Verwendung

```svelte
import SettingsPanel from '$lib/components/settings/SettingsPanel.svelte';

<SettingsPanel />
```
