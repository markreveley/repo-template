# Schema

**What this file is for.** The formats and contracts of the data the repo
holds or emits: file layouts, frontmatter fields, identifiers, JSON shapes,
CLI arguments and exit codes, anything another program reads. Changing it is
a breaking change for whatever reads the data, so the file says who that is.

**Changed by:** a breaking change, announced to whatever reads the data.

**Belongs here:** each format with an example that validates; every field
with whether it is required and what values it takes; the identifier rules;
the parsed shape a reader gets; the error and problem codes; the readers
the contract binds (downstream repos, CI, a viewer).

**Does not:** how to write the data by hand (`../docs/`); why the format is
as it is (`ARCHITECTURE.md`, decisions); rules about the data's content
rather than its form (`POLICY.md`).

**Form.** One section per format, each opening with a complete example
taken from a file that exists in the repo and is checked by its tests, then
the fields as a table. A "Readers" section at the end names what breaks
when the schema changes and how a change is announced.
