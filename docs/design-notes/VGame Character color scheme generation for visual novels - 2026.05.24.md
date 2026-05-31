# Character color scheme generation for visual novels

Source: https://claude.ai/chat/1665f555-5c54-44ff-8952-9763fe726220
Date: 2026.05.24
Extracted: 2026-05-31

---

## 1. User (2026.05.24)

I'm working on a visual-novel like game. Characters are auto generated randomly, then art is ai-generated automatically. just simple characters.

Game engine generates JSON, with character description, something like:

```
{
    "hair_length": "shoulder_length",
    "hair_color": "light_blonde",
    "eye_color": "brown",
    "dress_color": "...",
    "neckless": "none",
    "bracelet": "gold",
    ...
}
```

And so on. Now clothing is also auto generated. Here is my fashion-related question. When designing an overall consistent character looks, how would I do it? choose primary/secondary colors and have say black clothes (primary), with red accents/jewlery (secondary)? what is the usual way to do it? feel free to draw inspiration from design, fashion, game design, etc. Ask questions to understand the issue? this is more a brainstorming than real question

## 1. Claude

Good question to think through. There are a few real fashion/design principles that translate cleanly into procedural generation logic.

The big one is the 60-30-10 rule, which is genuinely how interior designers, stylists, and costume designers work: 60% dominant color (main dress/outfit), 30% secondary (jacket, skirt, contrasting piece), 10% accent (jewelry, shoes, lipstick, scarf). Visual hierarchy without chaos. Your generator can implement this almost directly — pick base, secondary, and accent, then assign to slots based on visual surface area.

But colors also need a relationship, not just ratios. This is color harmony, and there are well-defined schemes:

- Monochromatic — different shades of one hue. Elegant, safe.
- Analogous — neighbors on the wheel (blue/teal/green). Natural, cohesive.
- Complementary — opposites (red/green, blue/orange). Bold.
- Triadic — three evenly spaced. Playful.
- Neutral + pop — mostly black/white/beige with one bold accent. Modern, fashion-forward.

So instead of rolling colors randomly per slot, roll a harmony scheme, then derive colors from it. Three or four colors max per character — more reads as noise.

A few other rules real stylists actually follow that are easy to encode:

- Metals match. Gold and silver jewelry don't usually mix on one person. If you generate a necklace, bracelet, and earrings, lock them to one metal family unless you're going for eclectic on purpose.
- Formality consistency. Each item has an implicit formality (sneakers ≠ ballgown). Give items a 1–5 formality score and tighten the spread.
- Hair/skin coherence. "Color season" theory says warm-toned people (golden/red hair) look best in warm palettes, cool-toned in cool. Weight your palette generator by hair color and characters start feeling naturally put-together without you specifying it.

For architecture, two approaches worth considering:

Archetype-first — Define a handful of style archetypes (preppy, gothic, romantic, tomboy, elegant, casual). Each constrains palette, harmony, and formality. Then fill JSON slots. Pro: instant coherence, characters feel intentional. Con: less variety, you'll start seeing the templates.

Palette-first — Roll a harmony scheme, derive colors, roll formality, fill slots conforming to constraints. Pro: more emergent variety. Con: needs more downstream rules to avoid weird combos.

In practice I'd combine them: archetype picks the constraints, palette generator fills the values with bounded randomness. That's roughly how character creators in games like the Sims or Honkai Star Rail's character editor handle "preset → tweak" flows.

A few questions to narrow this down:

- What's the visual style — anime, semi-realistic, chibi, painterly? It changes how forgiving the palette needs to be (anime tolerates wild colors; realistic doesn't).
- Are clothes meant to telegraph personality (cute one wears pink, rebel wears leather), or purely decorative?
- How many characters share a scene at once? Cohesion across the cast matters more if you show groups; less if it's one-at-a-time.

## 2. User (2026.05.24)

A bit more context: visual style undecided, likely something semi-realistic, since AI art generator like realistic (apart from Pony etc). Maybe with light LoRA to take edge a bit off (so it doesn't look like instagram reel).

The setting is dark fantasy. Most NPC will be 'boring'. But there are special characters, usually wizards, high nobles, etc. They like to dress up basically, think cocktail parties with fantasy themes.

## 2. Claude

Dark fantasy actually solves a lot of your problem before you start, because the setting itself enforces a master palette: desaturated jewel tones, deep reds, oxblood, plum, forest green, indigo, blacks, with metallic accents (brass, tarnished silver, antique gold — not bright chrome or yellow gold). Once you constrain to that universe, even random rolls stay coherent. Think Witcher 3 / Dragon Age / Bloodborne — almost nothing in those games is "wrong" color-wise because the palette is pre-filtered.

A two-tier setup maps really naturally here:

Boring NPCs — single muted base color (browns, grays, dirty whites, faded blues), one cheap material (wool, linen, undyed leather), no jewelry or maybe one simple piece. Formality 1–2. The randomness budget is intentionally small. These should look like background actors.

Special characters — full 60-30-10 palette, multiple materials, a "signature" element, formality 4–5. This is where you spend the visual interest.

A few things specific to your stack worth thinking about:

Material matters more than color in dark fantasy. "Velvet," "brocade," "lace," "fur trim," "silk," "tarnished mail" — these words do enormous work in both the visual language and in AI prompts. I'd add a `materials` slot, not just colors. A noble in plain red cotton reads wrong; a noble in burgundy velvet reads immediately as a noble. Material is class signaling.

House/faction colors are gold. If your special characters are tied to noble houses or magical orders, give each faction a locked 2-color palette + signature motif. House Vorne wears black and oxblood with raven imagery; the Order of Cinders wears charcoal and burnt orange. Multiple characters from the same faction visually cohere, and players start reading the heraldry without you teaching it. This is how A Song of Ice and Fire / Game of Thrones costuming works.

Fantasy aesthetic archetypes are worth defining explicitly: courtly, witchy, occult, druidic, decadent, martial-ornate, scholarly-wizardly. Each one constrains palette + materials + accessory weight. The "cocktail party but fantasy" vibe maps to decadent court — theatrical, layered, revealing fabric choices, statement jewelry. Lean into it; don't be afraid of slightly over-the-top because semi-realistic SD models render restrained dark fantasy 100x more reliably than they render subtle modern fashion.

Prompt-engineering caveat worth flagging early: your JSON is going to become a prompt, and SD-family models start ignoring or scrambling details past ~20 specific attributes. So the JSON should probably have a priority order — the top 5-7 traits go in the prompt, the rest become flavor for dialogue/lore but not necessarily image gen. Over-specifying jewelry while leaving "velvet gown" implicit is a common failure mode.

Two questions back:

- Do you want the JSON to be the source of truth (everything in it gets rendered) or more of a character bible where the image gen only consumes a curated subset?
- For special characters, are they recurring (same character needs to look consistent across multiple generations) or one-shot? Consistency across regenerations is a separate, hairy problem.

## 3. User (2026.05.24)

It's a bit more sophisticated, JSON is fed to LLM as a structure, LLM then generates coherent, possibly multi-paragraph detailed character description. LLM is allowed to invent details, JSON is to inject enthropy/stability. The description generated by LLM becomes the "master copy". this goes into image gen. (Z-Image, or other modern generator, which can take a long detailed description) which generates template image. character standing straight on gray background, diffused lighting, full body shot, this kind of thing. Downstream "master copy" and "character template image" are used for scenes. Here we are mainly concerned with "master copy". currently i feed existing images to VLM and ask it to describe character in detail. but that works for quick test, not to generate lots of characters

## 3. Claude

That changes the shape of the problem significantly. With an LLM in the loop, the JSON isn't a spec anymore, it's a seed. You're not encoding fashion rules — you're giving the LLM enough constraint to make coherent choices and enough entropy to make distinctive ones. The LLM already knows what brocade is and that gold-trimmed velvet doesn't belong on a stablehand. Stop fighting it for that knowledge; lean on it.

That suggests a three-layer JSON:

Identity layer (immutable across regenerations) — face shape, build, hair, eyes, age, signature marks/scars. These are the anchors that have to survive regens, because if they drift, you've made a different person. This is what your template image locks in and what scene generation has to preserve.

Aesthetic layer — archetype tag (decadent_court, witchy, scholarly, martial_ornate, etc.), faction/house if any, formality tier, color harmony tag (`monochromatic_oxblood`, `cool_neutral_with_silver_accent`), one or two anchor materials (velvet, brocade, lacquered leather). This is high-level enough for the LLM to make consistent costume choices without you enumerating slots. "Decadent court witch, House Vorne, formality 5, oxblood-and-jet palette, velvet and lace" gives the LLM more useful constraint than fifteen color fields, and it's less likely to produce internally contradictory outputs.

Quirk slot(s) — one or two specific weird details. A milk-white left eye. Lips painted black. A pet raven on her shoulder. Smells of myrrh. A chipped front tooth. This is the most important field and the one most people skip. LLMs default to dark-fantasy boilerplate ("she wore a long black dress, her piercing eyes...") unless you give them something specific to anchor on. Quirks are anti-genericness. They're also what makes a character recognizable later — readers remember the woman with the raven, not the woman with the velvet gown.

A few other things worth raising:

The VLM-on-real-images approach is actually your most powerful lever, not a fallback. Run a few hundred dark fantasy artworks through a VLM to extract JSON-shape descriptions, and you get a realistic joint distribution of attributes. Then your generator samples from that distribution rather than rolling each field independently. The "peasant accidentally rolled gold brocade" problem disappears because the distribution itself encodes that nobles wear velvet and peasants don't. It also surfaces design vocabulary you wouldn't have thought to enumerate (mantles, gorgets, jeweled circlets, specific embroidery motifs). Even a small corpus dramatically beats hand-tuned weights.

Boring NPCs probably shouldn't go through the LLM step at all. A templated string straight from JSON ("middle-aged woman, brown hair tied back, faded gray wool dress, unremarkable") fed directly to image gen will read correctly as background, faster and cheaper. Save the LLM creativity budget — and the prose-master-copy storage — for characters who matter. You could literally branch on a `tier: background | named | major` field.

Layer separation pays off later. If identity and presentation are separated in JSON, you can later do "same character, hunting clothes" vs "same character, ballgown" by swapping the aesthetic layer while keeping identity locked. Worth designing for now even if you don't use it yet. This is also where you'd handle the character changing over the story (mourning, injury, promotion).

Negative constraints, optionally. A small `avoid:` field in the LLM prompt helps if you're seeing recurring tics — "no pointy hats, no generic 'piercing gaze', no anachronistic items." Modern LLMs need this less than older ones, but it's a useful escape hatch when you notice patterns.

Two questions:

- Batch (generate 500 characters offline, store) or live during play? It changes how much you care about per-character latency vs upfront pipeline complexity.
- How much character drift between the template image and downstream scene images is acceptable? That answer drives whether you need IP-Adapter/face embeddings/LoRAs on top of master-copy text, which is a different sub-problem but tightly coupled to how detailed your identity layer needs to be.

## 4. User (2026.05.24)

That is a good idea, to extract json from images, but i need a schema. this is this conversation about. what would be useful schema. Also, character clothing in permanent. what would be minimal PoC for a json, don't generate proper schema, just fields and example values suffice

## 4. Claude

Right, makes sense. Here's a minimal PoC shape — fields with example values for a single "decadent court" type character, the kind worth bothering with:

```
{
  // === IDENTITY (locked, survives regens) ===
  "sex": "female",
  "age_apparent": 35,                    // years, rough
  "build": "slender",                    // slender | average | stocky | muscular | heavyset
  "height": "tall",                      // short | average | tall
  "skin_tone": "pale",                   // pale | fair | olive | tan | brown | dark
  "skin_undertone": "cool",              // warm | cool | neutral
  "face_shape": "oval",                  // oval | round | heart | square | long
  "hair_length": "long",                 // shaved | cropped | short | shoulder | long | very_long
  "hair_color": "jet_black",
  "hair_style": "loose_with_braided_crown",
  "eye_color": "pale_grey",
  "distinguishing_marks": ["thin scar across left brow", "ink-black manicured nails"],

  // === AESTHETIC (the costume bible) ===
  "archetype": "decadent_court",         // decadent_court | witchy | scholarly | martial_ornate | druidic | occult | courtly_restrained | peasant | merchant | clergy
  "faction": "House Vorne",              // null for unaligned
  "social_tier": "high_noble",           // peasant | commoner | merchant | minor_noble | high_noble | royalty | clergy | outcast
  "formality": 5,                        // 1–5
  "palette_scheme": "monochromatic_dark",// monochromatic_dark | neutral_with_accent | analogous_jewel | complementary_bold | earth_muted
  "primary_color": "jet_black",
  "secondary_color": "oxblood",
  "accent_color": "tarnished_silver",
  "primary_material": "velvet",
  "secondary_material": "black_lace",
  "metal_family": "tarnished_silver",    // gold | rose_gold | silver | tarnished_silver | brass | iron | none
  "silhouette": "fitted_bodice_floor_length_skirt",
  "skin_exposure": "modest",             // modest | moderate | bold | revealing
  "condition": "pristine",               // pristine | worn | weathered | tattered | bloodied

  // === SIGNATURE (anti-genericness; 1–3 items) ===
  "signature_elements": [
    "high standing lace collar framing the face",
    "raven-feather mantle across one shoulder",
    "signet ring on left index finger, black opal"
  ],

  // === LAYERS (what's actually on the body) ===
  "outerwear": "fitted velvet mantle, asymmetric, raven-feather trim",
  "main_garment": "floor-length black velvet gown, oxblood underskirt visible at slit",
  "underlayer": "black lace high-neck blouse",
  "legwear": null,
  "footwear": "pointed leather boots, silver buckles",
  "headwear": null,
  "gloves": "black leather, elbow length",

  // === JEWELRY & ACCESSORIES ===
  "necklace": "tarnished silver chain with black opal pendant",
  "earrings": "silver drop, small",
  "rings": ["black opal signet, left index"],
  "bracelets": [],
  "belt": "black leather, silver buckle shaped as a raven",
  "carried_item": "lacquered black fan, painted with silver constellations",

  // === FACE / GROOMING ===
  "makeup": "dark plum lip, kohl-lined eyes, otherwise minimal",
  "facial_hair": null,
  "scent": "myrrh and cold iron",         // flavor for prose, not image

  // === LLM HINTS ===
  "personality_seed": ["composed", "predatory", "amused"],   // 2–3 adjectives, biases prose tone
  "avoid": ["pointy witch hat", "generic 'piercing gaze'", "anachronistic items"]
}
```

A few notes on why these fields and not others:

Why two color layers (palette_scheme + the three colors). The scheme tells the LLM the relationship; the specific colors anchor it. Having both means a regeneration with the same JSON tends to converge on similar outputs, but you can also swap just the scheme to redesign coherently.

Why `silhouette` as a string, not enum. Silhouette is the single most important visual variable in fashion and the hardest to enumerate. Let it be free text — your VLM extraction will naturally produce a useful vocabulary, and the LLM consumes it fine.

Why separate `signature_elements` from layers/jewelry. Layers are the body of the costume. Signature elements are what someone remembers. Keeping them in a dedicated field forces the generator (or VLM) to identify 1–3 actually distinctive things, and forces the LLM to emphasize them in prose. Without this you get costumes that are well-described but forgettable.

Why `skin_exposure` and `condition` as their own fields. Modesty and wear-state are read instantly by viewers and carry huge narrative weight (a tattered noble = a story; a pristine peasant = wrong). They cut across all other fields, so they deserve their own slot rather than being buried in free text.

Why `scent`, `personality_seed`, `avoid`. None are visual but all change LLM prose quality dramatically. Scent in particular costs nothing and makes prose feel three-dimensional.

What's intentionally not here. Body measurements (creepy and unreliable from VLM), specific brand-equivalent designers, voice/accent (separate concern), backstory (separate concern). Keep this schema about appearance.

For boring NPCs you'd use maybe 8 of these fields — identity + archetype + social_tier + a couple color/material/condition fields — and skip everything else. The richness scales with the character's importance, which is what you want.

One thing worth flagging since clothing is permanent: lock the aesthetic block as immutable in your data model the same way identity is. The "same character in different outfits" flexibility I mentioned last turn doesn't apply to your design, and bolting it on later is harder than designing without it.

## 5. User (2026.05.24)

I'm not sure we understand each other. Your JSON looks good for something a person would write. In my case game engine is generating them. so values like 'high standing lace collar framing the face' make no sense, unless we get llm to generate them, which is extra step and not PoC. What i think would be more suitable now, is maybe 3-7 fields for character (eyes, body color etc), 3-7 for clothing. that's it for now. they need to all be RNG-capable to be pulled from small value set. Maybe with constraints on colors you mentioned earlier

## 5. Claude

Got it, my mistake — I was writing for a human author, not a die-roller. Here's the actually-minimal PoC: every field rolls from a closed set, no free text anywhere.

```
// === CHARACTER (identity) ===
{
  "sex": "female",              // [male, female]
  "build": "slender",           // [slender, average, stocky]
  "skin_tone": "pale",          // [pale, fair, olive, tan, brown, dark]
  "hair_length": "long",        // [short, shoulder, long]
  "hair_color": "jet_black",    // see palette below
  "eye_color": "grey"           // [blue, grey, green, hazel, brown, amber]
}

// === CLOTHING ===
{
  "archetype": "decadent_court",   // [peasant, merchant, courtly, decadent_court, witchy, martial_ornate, scholarly]
  "primary_color": "jet_black",    // from palette
  "accent_color": "oxblood",       // from palette
  "metal": "tarnished_silver",     // [gold, silver, tarnished_silver, brass, none]
  "material": "velvet",            // [wool, linen, leather, silk, velvet, brocade, lace]
  "condition": "pristine"          // [tattered, worn, clean, pristine]
}
```

Shared color palette (both hair and clothing roll from this — keeps everything in-universe):
`jet_black, charcoal, oxblood, plum, forest_green, indigo, deep_blue, burnt_orange, ochre, cream, bone_white, ash_grey, dirty_brown, chestnut, jet_black, ash_blonde, copper_red`
(Hair pulls from the natural subset: black/charcoal/chestnut/copper_red/ash_blonde/ash_grey/bone_white. Clothing pulls from any.)

That's 12 fields total, all enums, all rollable independently — but with two cheap constraints that prevent 90% of the garbage outputs:

Constraint 1: archetype gates the other clothing fields. Don't roll them independently; roll archetype first, then roll within that archetype's allowed values. Sketch:

```
peasant         → material: [wool, linen],         metal: [none, brass],            condition: [tattered, worn]
merchant        → material: [wool, linen, leather],metal: [brass, silver],          condition: [worn, clean]
courtly         → material: [linen, silk],          metal: [silver, gold],           condition: [clean, pristine]
decadent_court  → material: [silk, velvet, brocade, lace], metal: [gold, silver, tarnished_silver], condition: [pristine]
witchy          → material: [wool, leather, velvet, lace], metal: [tarnished_silver, brass], condition: [worn, clean]
martial_ornate  → material: [leather, brocade],    metal: [silver, brass, tarnished_silver], condition: [worn, clean, pristine]
scholarly       → material: [wool, linen, velvet], metal: [brass, silver],          condition: [worn, clean]
```

This single table is what makes characters feel intentional instead of random. A peasant in gold brocade is the failure mode you want to eliminate first.

Constraint 2: primary + accent must follow a harmony rule. Instead of rolling two independent colors, roll the pair. Three pre-baked harmony types are enough:

```
monochromatic → both colors from same family    (jet_black + charcoal, plum + oxblood)
neutral+pop   → primary is neutral, accent vivid (charcoal + burnt_orange, bone_white + oxblood)
jewel_pair    → two saturated jewel tones        (oxblood + forest_green, indigo + plum)
```

Roll harmony type, then roll a valid pair from that type's pair list. Done.

So the actual generation order is:

1. Roll identity fields independently (6 rolls).
2. Roll archetype.
3. Roll material, metal, condition from archetype-allowed sets.
4. Roll harmony type, then roll a color pair from it.

12 enum fields, ~4 lookup tables, no LLM, no free text, and the outputs will already feel coherent enough to send through your existing LLM-expansion step. When you outgrow it you add fields (silhouette, accessories, headwear) the same way — enum + archetype gating.

## 6. User (2026.05.24)

This is still not quite that. I only need to cover high born. I don't need "wear", the reference image will always be "pristine", wear is added later

Character:
Overall:
sex
age (later)
build/body_proportions
height (later)
skin_tone
body_hair (later)
body_scars (later)
body_tattoos (later)
Face:
face_shape
hair_length
hair_color
hair_style
eye_color
face_hair (later)
face_scars (later)
face_tattoos (later)
Other:
other (later, horns, pointy ears)
makeup (later, eyes, lips, nails, face/body)
jewlery/piercings (later, ears, nose, neckless, headband, need to be consistent with the rest of character)

So far got this, anything major missing? piercings omitted for now, but i think they should go to the "face" part rally. Briefly

## 6. Claude

Looks solid. Genuine gaps, briefly:

Eyebrows — visible on every character, can deliberately mismatch hair (dyed hair vs natural brows, plucked-thin vs full), and dark fantasy makes a lot of use of them (drawn-on arches, shaved-and-redrawn, etc). Goes in Face. Even a 2-value enum (thick / thin) is enough; color usually inherits from hair.

Skin undertone (warm / cool / neutral) — separate from skin_tone. Worth its own field because it's what gates "does this character look right in gold vs silver, in oxblood vs plum." Cheap to roll, pays off when you connect to palette later. Goes in Overall.

That's about it for image-relevant fields. Lip shape, nose shape, eye shape — Z-Image and similar will derive these from face_shape + ethnicity cues in the prompt; enumerating them adds tokens without adding signal at PoC stage.

On grouping:

- Piercings → split. Face piercings (ears, nose, lip, brow, septum) belong in Face. Body piercings (navel, etc.) in Overall — though for highborn template shots they're rarely visible so probably skippable.
- Necklace / collar / choker → not really Face. It's a neck/décolletage item. I'd put it under jewelry as its own slot rather than forcing it into Face or Overall.
- Headband / circlet / tiara → Face is fine, or call it "head" alongside hair. Highborn especially get circlets, so worth its own slot eventually.
- Earrings → Face (they sit on the face plane visually).

One framing note: "build/body_proportions" and "height" are doing similar work. Build = mass distribution, height = scalar. Keep them separate as you have them — just flagging that "body_proportions" can read as redundant with build. I'd rename to just `build`.

Nothing else missing for a pristine highborn template. The "later" fields are correctly deferred.

## 7. User (2026.05.24)

What is skin undertone? briefly?

## 7. Claude

Skin undertone is the underlying hue beneath the surface color of the skin — separate from how light or dark the skin is.

Three categories:

- Warm — golden, peachy, yellow underneath. Veins look greenish.
- Cool — pink, red, bluish underneath. Veins look blue/purple.
- Neutral — mix of both, no strong pull either way.

Two people can have the same skin_tone ("fair") but different undertones, and they'll look noticeably different — and look right in different colors. Warm undertones pair with gold, oxblood, burnt orange, forest green. Cool undertones pair with silver, plum, indigo, deep blue. It's why "I look washed out in this shirt" happens even when the color is objectively nice.

For your generator it's the bridge between character identity and palette: roll undertone, and it constrains which metal and which clothing colors will look intentional rather than accidental.
