# README.md Coverage Audit — Interverse Monorepo

**Date:** 2026-02-18
**Scope:** `/root/projects/Interverse/plugins/*`, `hub/clavain/`, `services/intermute/`, `infra/marketplace/`

---

## Summary

- **Total directories checked:** 34
- **Missing README.md:** 22
- **Have README.md:** 12

---

## Missing README.md (22 directories)

All missing entries are plugin subdirectories. Hub, services, and infra directories are covered.

| # | Module | Path |
|---|--------|------|
| 1 | intercheck | `/root/projects/Interverse/plugins/intercheck` |
| 2 | intercraft | `/root/projects/Interverse/plugins/intercraft` |
| 3 | interdev | `/root/projects/Interverse/plugins/interdev` |
| 4 | interflux | `/root/projects/Interverse/plugins/interflux` |
| 5 | interform | `/root/projects/Interverse/plugins/interform` |
| 6 | interject | `/root/projects/Interverse/plugins/interject` |
| 7 | interkasten | `/root/projects/Interverse/plugins/interkasten` |
| 8 | interleave | `/root/projects/Interverse/plugins/interleave` |
| 9 | interline | `/root/projects/Interverse/plugins/interline` |
| 10 | interlock | `/root/projects/Interverse/plugins/interlock` |
| 11 | intermap | `/root/projects/Interverse/plugins/intermap` |
| 12 | intermem | `/root/projects/Interverse/plugins/intermem` |
| 13 | intermux | `/root/projects/Interverse/plugins/intermux` |
| 14 | internext | `/root/projects/Interverse/plugins/internext` |
| 15 | interpeer | `/root/projects/Interverse/plugins/interpeer` |
| 16 | interphase | `/root/projects/Interverse/plugins/interphase` |
| 17 | intersearch | `/root/projects/Interverse/plugins/intersearch` |
| 18 | interserve | `/root/projects/Interverse/plugins/interserve` |
| 19 | interslack | `/root/projects/Interverse/plugins/interslack` |
| 20 | interstat | `/root/projects/Interverse/plugins/interstat` |
| 21 | intersynth | `/root/projects/Interverse/plugins/intersynth` |
| 22 | intertest | `/root/projects/Interverse/plugins/intertest` |

---

## Present README.md (12 directories)

| Module | Path |
|--------|------|
| interdoc | `/root/projects/Interverse/plugins/interdoc` |
| interfluence | `/root/projects/Interverse/plugins/interfluence` |
| interlens | `/root/projects/Interverse/plugins/interlens` |
| interpath | `/root/projects/Interverse/plugins/interpath` |
| interpub | `/root/projects/Interverse/plugins/interpub` |
| interwatch | `/root/projects/Interverse/plugins/interwatch` |
| tldr-swinton | `/root/projects/Interverse/plugins/tldr-swinton` |
| tool-time | `/root/projects/Interverse/plugins/tool-time` |
| tuivision | `/root/projects/Interverse/plugins/tuivision` |
| clavain | `/root/projects/Interverse/hub/clavain` |
| intermute | `/root/projects/Interverse/services/intermute` |
| marketplace | `/root/projects/Interverse/infra/marketplace` |

---

## Observations

1. **Hub, services, and infra are covered.** `clavain`, `intermute`, and `marketplace` all have README.md files. The gap is entirely in the plugins layer.

2. **22 out of 31 plugin directories lack README.md** — a 71% gap. This represents a significant discoverability and onboarding deficit for the plugin ecosystem.

3. **Plugins with README.md tend to be the more mature/published ones** — `interdoc`, `interfluence`, `interpub`, `interwatch`, `tldr-swinton`, `tool-time`, `tuivision`, `interlens`, `interpath`. The missing ones skew toward newer or more experimental modules.

4. **`intermem` appears in the missing list** — this module is not listed in the monorepo structure in `CLAUDE.md`, suggesting it may be a recently added or experimental module.

---

## Recommended Next Steps

- Prioritize README.md for actively published plugins: `interflux`, `interlock`, `intermap`, `intermux`, `interpeer`, `interserve`
- Use `interdoc` (AGENTS.md generator) to scaffold initial READMEs for remaining modules
- Consider adding a CI check or marketplace gate that requires README.md before a plugin can be listed
