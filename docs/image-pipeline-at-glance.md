**Pipeline at a glance:**

The engine emits a small structured JSON describing a location along orthogonal axes — natural backdrop (climate, terrain, vegetation), human-built style (architecture), what's at the spot (location), and the state of any built structures (condition). Fields are intentionally minimal and reusable: each value combines freely with the others, so the same schema covers wilderness, roads, villages, and castles without per-case branching.

An LLM acts as art director. It receives the JSON plus an inlined style brief and inlined field definitions, and converts the structured input into a single detailed natural-language image prompt. Its job is to invent concrete visual specifics (tree species, building forms, weathering, ground surfaces) consistent with the fields, while obeying a fixed set of rules: bake neutral overcast daylight into the base, leave figures out, express mood through palette and decay rather than darkness, and reconcile odd field combinations rather than treating them as errors.

A text-to-image model generates the base image from that prompt. The base is deliberately flat-lit and atmospherically neutral — not because that's the desired aesthetic, but because it's the most editable starting state.

A second pass uses an instruction-following edit model to transplant weather and time-of-day variants onto the base: overcast storm, blood moon, night, heavy rain, etc. Each variant uses a shared prompt grammar — *re-render the same scene, preserve every object, light source is X, palette is Y, this is a photograph of state X not a tint of the original*. The grammar is consistent across variants so the director can template rather than hand-write each one, and the closing "this is X not Y" line defends against the model's default failure mode of applying a color filter instead of relighting.

When a variant goes wrong or an input image needs to be brought into the pipeline from outside, a neutralisation prompt rebases any arbitrary image back to the flat overcast template, making the whole pipeline reversible: any state → neutral → any other state, without re-running base generation.

Open-weight edit models on the bench (Flux Kontext dev, Flux 2 klein, Qwen-Image-Edit, HunyuanImage-3 Instruct, Z-Image-Edit) are tested head-to-head on identical bases and prompts. The architectural conclusion held in testing so far: weather transplants within a lighting regime work well; the day↔night relighting jump needs a prompt rewritten as a *re-render* rather than an *adjustment* to avoid the blue-overlay failure, and may eventually be better handled by generating night bases from scratch at shared seed rather than editing from the day base.

The whole approach trades richness for orthogonality: small JSON, one editable base per location, weather as a separate cheap layer.
