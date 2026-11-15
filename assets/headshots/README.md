# Collaborator headshots

Keep downloaded originals in `raw/`. The files below are unmodified; pixel
dimensions alone do not establish the resolution of the photographs embedded
in a composite. Retrieved November 13, 2026.

| File | Subject | Pixels | Source |
| --- | --- | --- | --- |
| `raw/kuo-frances.jpg` | Frances Y. Kuo | 200 × 250 | [UNSW profile](https://www.unsw.edu.au/staff/frances-kuo), [original image](https://api.research.unsw.edu.au/sites/default/files/images/profile/1315891244_frances_kuo.jpg) |
| `raw/kuo-nuyens-oden-2025.png` | Frances Y. Kuo (upper left) and Dirk Nuyens (lower right) | 1728 × 2304 | [Oden Institute seminar, March 11, 2025](https://oden.utexas.edu/news-and-events/events/2062---Frances%20Y.%20Kuo%20%26%20Dirk%20Nuyens/), [original composite image](https://oden.utexas.edu/media/events/event/Untitled_design_1_ppNrvTR.png) |
| `raw/millet-megan.png` | Megan Millet | 1254 × 1254 | Supplied as `portrait_photo_Millet.png` in her November 13, 2026 reply to “Headshot for Monday’s colloquium talk”, for slides available online |

The Oden image is the full-size published composite, not the standalone
original of Dirk's portrait. That standalone original has not been located.
The Frances photo also appears on her [personal UNSW
homepage](https://web.maths.unsw.edu.au/~fkuo/Frances_Kuo.jpg); the two downloads
were byte-identical, so only one is retained.

## Prepared portraits

| File | Subject | Pixels | Input |
| --- | --- | --- | --- |
| `processed/kuo-frances.png` | Frances Y. Kuo | 1254 × 1254 | `raw/kuo-frances.jpg` |
| `processed/nuyens-dirk.png` | Dirk Nuyens | 1254 × 1254 | Dirk's lower-right portrait in `raw/kuo-nuyens-oden-2025.png` |
| `processed/millet-megan.png` | Megan Millet | 1254 × 1254 | Byte-identical copy of her already square original |

Frances and Dirk's portraits were prepared with the built-in image editor on
November 13, 2026 and visually reviewed. These two are AI-processed derivatives,
not pixel-identical crops of the
original photographs. The originals above remain unchanged. Use the portraits
at small slide-headshot size; the larger output dimensions do not establish
additional photographic detail.

Prompt set: make square academic headshots showing hair, face, neck and upper
shoulders, centered on the face; preserve identity, expression, clothing,
lighting, colors and original background; request crop and scale only, with no
beautification, face reconstruction, retouching or invented detail. For Dirk,
select only his lower-right photograph and remove the turquoise composite
background and white border. No captions, names, graphics or watermarks.

Megan's supplied portrait is unchanged, including in `processed/`; it needed
no cropping, resizing, retouching, or AI processing. Its SHA-256 is
`62ed0526e2a1975889bd337150ea2ac8f01f431b9cb800f46befcb9a5a489ddb`.

## Master list, iCloud archive, and publishing copies

Follow `classlib/docs/collaborators.md`. The pinned
`classlib/classlib/quarto/metadata/hickernell-collaborators.yml` supplies names
and stable IDs. Master originals and prepared portraits are in iCloud Drive's
`Collaborator Headshots` archive, with acquisition/crop provenance and hashes
in its `catalog.yml`. MCQMC26 is a historical source collection, rather than
the master catalog for future talks. The iCloud archive retains Megan’s
supplied PNG and provenance.

`data/collaborators.yml` explicitly selects this talk's photos. The shared
helper refreshes their publishing copies in `processed/`, generates the
QMCPy caption include, and writes `manifest.json`. The slide pre-render check
verifies selected names, hashes and generated markup without requiring iCloud.
Custom recent-contribution names use the same master metadata. Existing
historical raw sources documented above remain for provenance; new master
originals go to iCloud, not into the talk repository.

Samuel Vangu's original was acquired from his [website](https://samuel-vangu.github.io/)
and its [profile photograph](https://samuel-vangu.github.io/assets/img/profile.jpg)
on November 15, 2026. The original is `originals/vangu-samuel.jpg` in the
iCloud archive. The ready-to-use `vangu-samuel.jpg` is a reviewed 500×500 crop
of box `(1000, 240, 1600, 840)` in the 2000×1500 original, prepared with the
archive's existing crop-only helper (Lanczos resize, JPEG quality 92), with
no AI editing. Both hashes and the source are recorded in its catalog;
the selected publishing copy's hash is in this talk's manifest.

## QMCPy introduction

The eleven JPG portraits used in `slides/_includes/qmcpy-contributors.qmd` are
byte-identical copies of the existing processed MCQMC26 portraits. Fred
confirmed the initial selection on November 13, 2026: Sou-Cheng Choi, Yuhan Ding, Joshua Herman, R. Jagadeeswaran, Aadit Jain, Larysa Matiukha, Pieterjan Robbe, Aleksei Sorokin, Laasya Priya Vemuri, Yifei Xiong. On November 14 he added Art Owen, recognizing contributions of ideas as well as code. Art's portrait is also copied unchanged from the processed MCQMC26 collection.
Laasya appears once. This is the selected presentation photo group, not an
exhaustive list of every contributor to the library.

On November 15, 2026, Fred added Brandon Sharp, Richard Varela and Samuel
Vangu, bringing the selected QMCPy group to fourteen. Its explicit ID list features
Choi and Sorokin in columns five and six beside the introductory text; the
remaining twelve are alphabetical by surname in the two rows below. All
share the same six-column grid, so portrait columns align. Sharp's and Varela's
iCloud masters are unchanged copies of the earlier MCQMC26 files. All display
sizes and circular styling match. Ishaan and Joshua Park remain deferred.

## Recent-work contribution rows

The opening acknowledgment uses Frances Kuo's and Dirk Nuyens's prepared
portraits above and `processed/kritzer-peter.jpg`, an unmodified, byte-identical
copy from the processed MCQMC26 portrait collection. The names accompany the
portraits so the audience can identify the past collaborators. Their display
order is alphabetical by surname: Kritzer, Kuo, Nuyens. The student contribution
rows remain chronological: Matiukha, Pride, Kang, Millet.

The portrait bullets on the contribution slide reuse Larysa Matiukha’s JPG
and Megan Millet’s supplied PNG already present here. Jiangrui Kang’s
`processed/kang-jiangrui.jpg` and Anders Pride’s `processed/pride-anders.jpg`
are unmodified, byte-identical copies from the processed MCQMC26 portrait
collection. Fred supplied the contribution text in the slide source; the
wording and four portrait rows were reviewed for clarity and fit. Only
Larysa's contribution has a paper citation, arXiv:2610.10543; the other
results are still being written up.
