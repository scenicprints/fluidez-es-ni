# Fluidez — Nicaraguan Spanish (es-ni)

Content repository for the Fluidez language app.

/ content
  / manifest.json        index of all lessons & scenarios
  / dictionary/core.json full word dictionary
  / patterns/core.json   grammar pattern explainers
  / lessons/*.json       81 story lessons (Phases 0-7)
  / scenarios/*.json     40 branching conversation scenarios

The app reads content/manifest.json first, then fetches listed files.
To add content: add the file, then add its entry to manifest.json.
