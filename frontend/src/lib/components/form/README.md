# 📝 Form Components

> Reusable form field components for dynamic rendering

## 📋 Contents

| File | Description |
|------|-------------|
| `FieldRenderer.svelte` | Dynamic field renderer based on type |
| `FieldText.svelte` | Text input field |
| `FieldTextarea.svelte` | Multiline text area |
| `FieldSelect.svelte` | Dropdown select |
| `FieldDatetime.svelte` | Date/time picker |
| `FieldReadonly.svelte` | Read-only display |
| `index.ts` | Barrel export |

## 🏗️ Architecture

```
FieldRenderer (dynamic dispatcher)
├── FieldText     (type: "text")
├── FieldTextarea (type: "textarea")
├── FieldSelect   (type: "select")
├── FieldDatetime (type: "datetime")
└── FieldReadonly (type: "readonly")
```

## 🔧 Usage

```svelte
<script>
  import FieldRenderer from '$lib/components/form/FieldRenderer.svelte';

  const field = {
    name: 'title',
    type: 'text',
    label: 'Task Title',
    required: true
  };
</script>

<FieldRenderer
  {field}
  value={task.title}
  onchange={(v) => task.title = v}
/>
```

## 🎯 Props Pattern

All field components share the same props interface:

```typescript
interface FieldProps {
  field: Field;
  value: unknown;
  onchange: (value: unknown) => void;
  disabled?: boolean;
}
```
