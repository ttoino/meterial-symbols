<script lang="ts">
    import "../app.css";

    const { children } = $props();
</script>

<svelte:head>
    <title>Meterial Symbols</title>
</svelte:head>

<main class="flex h-full w-full flex-col items-center justify-center gap-8 p-4">
    <h1
        class="text-center text-title-l medium:text-display-s large:text-display-l"
    >
        Meterial Symbols
    </h1>

    {@render children?.()}
</main>
