<script lang="ts">
    import { fromHex } from "$lib/strings";
    import symbols from "$lib/symbols.json";
    import {
        ConnectedButtonGroup,
        Icon,
        Slider,
        ToggleIconButton,
    } from "svelte-m3c";

    let symbolName = $state(symbols[0].name);

    let symbol = $derived(
        symbols.find((s) => s.name === symbolName) ?? symbols[0],
    );

    let progress = $state(0);
</script>

{#snippet infolist(title: string, items: string[])}
    <p class="inline-flex gap-1">
        <span class="text-title-m">{title}:</span>
        <span class="text-body-l">
            {#each items as item, index (index)}
                {#if index != 0},
                {/if}
                <span
                    class="rounded-xs bg-surface-container-highest px-1 font-mono"
                >
                    {item}
                </span>
            {/each}
        </span>
    </p>
{/snippet}

<div
    style:--progress={progress}
    class="flex w-full max-w-(--breakpoint-medium) flex-col items-center gap-8 px-8"
>
    <Icon class="icon-24" icon={fromHex(symbol.codepoints[0])} />

    <Slider
        containerClass="w-64 !min-w-0 max-w-full"
        max={100}
        min={0}
        type="single"
        bind:value={progress}
    />

    {@render infolist(
        "Codepoints",
        symbol.codepoints.map((c) => c.replace("0x", "U+")),
    )}
    {@render infolist("Ligatures", symbol.ligatures)}

    <ConnectedButtonGroup
        class="overflow-x-auto"
        color="secondary"
        type="single"
        variant="tonal"
        bind:value={() => symbolName, (v) => v && (symbolName = v)}
    >
        {#each symbols as symbol (symbol.name)}
            <ToggleIconButton
                icon={fromHex(symbol.codepoints[0])}
                value={symbol.name}
            />
        {/each}
    </ConnectedButtonGroup>
</div>
