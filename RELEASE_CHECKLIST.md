# Release checklist

## Complete

- [x] Positioned FreeCAD assembly included
- [x] Unique print models exported as STEP and STL
- [x] Print orientations normalized to origin
- [x] Repeated geometries deduplicated with quantities in CSV
- [x] Source and prebuilt 20-pixel firmware included
- [x] Firmware vector address and UF2 payload verified
- [x] BOM, printing, electronics and assembly documentation included
- [x] License mapping and full license texts included
- [x] Final day/night photographs included
- [x] Construction-image sequence included
- [x] Muted H.264 staircase animation included
- [x] Publication media stripped of EXIF/container metadata
- [x] Main README embeds the release hero and overview images
- [x] Root release verifier included
- [x] SHA-256 manifest regenerated
- [x] Local release verification passed

## Human review before publication

- [ ] Review every file under `images/` and remove any view that should not be public
- [ ] Confirm repository name, description and publication host
- [ ] Initialize Git repository and inspect the complete staged diff
- [ ] Create the `v1.0.0` commit and annotated tag
- [ ] Publish the repository and verify rendered Markdown/media links remotely

After deleting or editing any release file, run:

```bash
python3 tools/update_checksums.py
python3 tools/verify_release.py
```
