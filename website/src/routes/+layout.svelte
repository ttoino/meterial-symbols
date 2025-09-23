<script lang="ts">
    import "../app.css";

    const { children } = $props();
</script>

<main class="flex h-full w-full flex-col items-center justify-center gap-8 p-4">
    <h1
        class="text-center text-title-l medium:text-display-s large:text-display-l"
    >
        Meterial Symbols
    </h1>

    {@render children?.()}
</main>
