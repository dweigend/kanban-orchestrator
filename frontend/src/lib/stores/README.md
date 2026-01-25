# 📦 Stores

> Svelte 5 state management with runes

## 📋 Contents

| File | Description |
|------|-------------|
| `schema.svelte.ts` | Dynamic task schema store |
| `settings.svelte.ts` | Application settings store |

## 🏗️ Architecture

Using Svelte 5 runes for reactive state:

```typescript
// Schema store
export const schemaStore = createSchemaStore();
// - schema: TaskSchema | null
// - loading: boolean
// - load(): Promise<void>

// Settings store
export const settingsStore = createSettingsStore();
// - settings: Settings
// - loading: boolean
// - load(): Promise<void>
// - save(): Promise<void>
```

## 🔧 Usage

```svelte
<script>
  import { schemaStore } from '$lib/stores/schema.svelte';
  import { settingsStore } from '$lib/stores/settings.svelte';

  // Access reactive state
  const schema = schemaStore.schema;
  const settings = settingsStore.settings;
</script>

{#if schemaStore.loading}
  <p>Loading...</p>
{:else}
  <p>Fields: {schema?.sections.length}</p>
{/if}
```

## 🎯 Pattern

Stores use the factory pattern with runes:

```typescript
function createStore() {
  let data = $state<Data | null>(null);
  let loading = $state(false);

  return {
    get data() { return data; },
    get loading() { return loading; },
    async load() { /* ... */ }
  };
}
```
