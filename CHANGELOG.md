# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0](https://github.com/rbarcante/claude-conductor/compare/v1.5.0...v1.6.0) (2026-03-30)


### Features

* **cli:** Add 6 batch CLI commands for token optimization ([ce50954](https://github.com/rbarcante/claude-conductor/commit/ce50954225dfc195de3f682998acab2b509ca41a))
* **codeReview:** Add save review prompt to codeReview and deduplicate with implement ([#63](https://github.com/rbarcante/claude-conductor/issues/63)) ([b6c1a07](https://github.com/rbarcante/claude-conductor/commit/b6c1a0713152905cc62fba011b54ec9b1d235369))
* **commands:** Integrate Plan Mode into newTrack workflow ([#59](https://github.com/rbarcante/claude-conductor/issues/59)) ([2a88d21](https://github.com/rbarcante/claude-conductor/commit/2a88d211f5dab56738f12fecdd57a09c1df7945d))
* **commands:** Rewrite implement, codeReview, setup protocols for token optimization ([8c7d7d2](https://github.com/rbarcante/claude-conductor/commit/8c7d7d2a31ce503b50564e92eb02b4dfcf9a449b))
* Remove conductor-specific git commits ([56911a3](https://github.com/rbarcante/claude-conductor/commit/56911a356fe7748941c56fdbf8fb95e4e89778c6))
* Remove conductor-specific git commits from workflow protocols ([22d2b59](https://github.com/rbarcante/claude-conductor/commit/22d2b59aaaa2c9c22257594c20e35fb11807830d))
* **skills:** Add glab-cli skill for GitLab CLI reference ([#64](https://github.com/rbarcante/claude-conductor/issues/64)) ([591955a](https://github.com/rbarcante/claude-conductor/commit/591955a59dcbbe5cd8e2c8a01d08ba248fbde99e))
* Token optimization CLI batch commands and protocol rewrites ([e473b67](https://github.com/rbarcante/claude-conductor/commit/e473b67df190c18e4f53a71eb52519cf60512aa0))


### Bug Fixes

* Address code review findings across CLI codebase ([368f73e](https://github.com/rbarcante/claude-conductor/commit/368f73e7b22e57ec800833a370ab82ee16c142c1))
* **ci:** Apply black formatting to pass lint check ([ab994b9](https://github.com/rbarcante/claude-conductor/commit/ab994b951c5202983e58fe72b3b5d4ee841e018d))
* **commands:** Address code review findings — security, quality, and test coverage ([da4f291](https://github.com/rbarcante/claude-conductor/commit/da4f29104e3253609623c35e9b2ae2c9080f9ab6))


### Reverts

* **version:** Restore 1.5.0 — version bump handled by CI ([e75b984](https://github.com/rbarcante/claude-conductor/commit/e75b9840c57c7ab33ab64f3f30898748556ea637))


### Code Refactoring

* **conductor:** Add warm start mode to implement.md for newTrack flow ([b599bc1](https://github.com/rbarcante/claude-conductor/commit/b599bc175b7384b5a832ecb6bb32ae9ae23e4316))
* **conductor:** Create track 'Enforce AskUserQuestion for all questions in newTrack.md' ([0f3a1eb](https://github.com/rbarcante/claude-conductor/commit/0f3a1ebf06abe4439a90d862bebf7c6e3eeaf18e))
* **conductor:** Create track 'Optimize implement.md context loading after newTrack flow' ([17ccb1f](https://github.com/rbarcante/claude-conductor/commit/17ccb1f8afc4093e2c07cda455cefa97565f12fa))
* **conductor:** Enforce AskUserQuestion globally via patterns template ([16d4f91](https://github.com/rbarcante/claude-conductor/commit/16d4f916f0751f227923a055a3004c1da608fa1d))
* **conductor:** Remove residual inline AskUserQuestion enforcement from newTrack.md ([17bd9c2](https://github.com/rbarcante/claude-conductor/commit/17bd9c25eb35ee0a338b80009ee600189f4c3887))
* **conductor:** Remove tracks.md registry, replace with directory scan (v2.0.0) ([d053532](https://github.com/rbarcante/claude-conductor/commit/d053532c995cddc90c7505ea52d49768e47d4bb4))
* Enforce parallel execution in codeReview command ([#62](https://github.com/rbarcante/claude-conductor/issues/62)) ([5ebb5c5](https://github.com/rbarcante/claude-conductor/commit/5ebb5c55fcd364abb2deb7d73139445304501bb2))

## [1.5.0](https://github.com/rbarcante/claude-conductor/compare/v1.4.0...v1.5.0) (2026-02-20)


### Features

* **skills:** Add ACLI Jira skill for CLI command reference ([#50](https://github.com/rbarcante/claude-conductor/issues/50)) ([f8e2eb7](https://github.com/rbarcante/claude-conductor/commit/f8e2eb76d2ae79ca4fd2c0e62275921b59f62625))

## [1.4.0](https://github.com/rbarcante/claude-conductor/compare/v1.3.0...v1.4.0) (2026-02-20)


### Features

* Auto code review, XML tag refactoring, and tracks parser fix ([ea00c31](https://github.com/rbarcante/claude-conductor/commit/ea00c31fde4012e6476027cfce8452ca286c8852))


### Bug Fixes

* **tracks-parser:** Parse Markdown table format in TracksParser ([#47](https://github.com/rbarcante/claude-conductor/issues/47)) ([a83447d](https://github.com/rbarcante/claude-conductor/commit/a83447da03e559e2897c46b752024f18a479387e))

## [1.3.0](https://github.com/rbarcante/claude-conductor/compare/v1.2.1...v1.3.0) (2026-02-19)


### Features

* **implement:** Add auto code review integration on track completion ([#39](https://github.com/rbarcante/claude-conductor/issues/39)) ([d24d622](https://github.com/rbarcante/claude-conductor/commit/d24d622c7547f1d177c44f4b726653cf2b44da6d))


### Code Refactoring

* **newTrack:** Add XML tags for structured prompt parsing ([#38](https://github.com/rbarcante/claude-conductor/issues/38)) ([d66d079](https://github.com/rbarcante/claude-conductor/commit/d66d079c022ee8de80b5b83447d39e61c9a34349))
* **setup:** Apply XML tags following newTrack.md pattern ([#40](https://github.com/rbarcante/claude-conductor/issues/40)) ([a11e719](https://github.com/rbarcante/claude-conductor/commit/a11e719591c687fc20a90f66e4129b901758387d))

## [1.2.1](https://github.com/rbarcante/claude-conductor/compare/v1.2.0...v1.2.1) (2026-02-12)


### Bug Fixes

* **release:** Point release workflow to config files and sync versions ([4ed13fb](https://github.com/rbarcante/claude-conductor/commit/4ed13fb6eae65e8b32a7f561f4e5f0ee69e140d7))

## [1.2.0](https://github.com/rbarcante/claude-conductor/compare/v1.1.0...v1.2.0) (2026-02-12)


### Features

* **marketplace:** Add marketplace.json for native plugin installation and updates ([b868880](https://github.com/rbarcante/claude-conductor/commit/b868880f3350fab6b053cf4dbe80d34d6831478a))
* **marketplace:** Add marketplace.json for native plugin installation and updates ([eccbf76](https://github.com/rbarcante/claude-conductor/commit/eccbf76683a9b91e4b8bc1dd243cc55ed5a0f287))

## [1.1.0](https://github.com/rbarcante/claude-conductor/compare/v1.0.1...v1.1.0) (2026-02-07)


### Features

* **agents:** Add code-quality-analyzer specialist agent for code smell and maintainability analysis ([41952a6](https://github.com/rbarcante/claude-conductor/commit/41952a6a3c6f49e7668a46a7b2cef5cf595523c5))
* **agents:** Add security-scanner agent for OWASP-aligned vulnerability detection ([98f02c7](https://github.com/rbarcante/claude-conductor/commit/98f02c76e6fa2e23d4255a7aaf938278261ae482))
* **agents:** Add test-coverage-analyzer agent for coverage gap identification ([98f02c7](https://github.com/rbarcante/claude-conductor/commit/98f02c76e6fa2e23d4255a7aaf938278261ae482))
* **agents:** Add git-history-analyst agent for commit analysis and revert list building ([9356980](https://github.com/rbarcante/claude-conductor/commit/9356980144583d45fccbb435b846b7b7b6c98988))
* **agents:** Add codebase-pattern-detector agent for architecture and naming convention detection ([9356980](https://github.com/rbarcante/claude-conductor/commit/9356980144583d45fccbb435b846b7b7b6c98988))
* **commands:** Integrate parallel sub-agents into codeReview command ([9b3fe58](https://github.com/rbarcante/claude-conductor/commit/9b3fe58a16353f509fd7624654450daa332b2d24))
* **commands:** Add quality gate sub-agents to implement and revert commands ([9fd6fb8](https://github.com/rbarcante/claude-conductor/commit/9fd6fb840d44efa8ab474885398414ea7780f190))
* **commands:** Add parallel pattern detection to setup command ([9e6a300](https://github.com/rbarcante/claude-conductor/commit/9e6a300ea82c38c1cc9743827c2a6bec2e81e648))
* **commands:** Add fast-path branch check and lazy skill loading to implement command ([#17](https://github.com/rbarcante/claude-conductor/issues/17)) ([4d1df81](https://github.com/rbarcante/claude-conductor/commit/4d1df81fe2de81f7b06c00f92c56fb0ec8a71e0b))
* **conductor:** Reduce token usage in newTrack workflow by 74% ([#16](https://github.com/rbarcante/claude-conductor/issues/16)) ([7aa16ed](https://github.com/rbarcante/claude-conductor/commit/7aa16ed606953ada5fe358156d8e4eeb26e34c25))
* **protocols:** Add verify-setup protocol ([4d1df81](https://github.com/rbarcante/claude-conductor/commit/4d1df81fe2de81f7b06c00f92c56fb0ec8a71e0b))
* **protocols:** Add Skill Loading Protocol for lazy skill activation ([7aa16ed](https://github.com/rbarcante/claude-conductor/commit/7aa16ed606953ada5fe358156d8e4eeb26e34c25))
* **protocols:** Add Pattern Resolution Protocol ([7aa16ed](https://github.com/rbarcante/claude-conductor/commit/7aa16ed606953ada5fe358156d8e4eeb26e34c25))
* **skills:** Add conductor-methodology SKILL-SUMMARY for lightweight loading ([7aa16ed](https://github.com/rbarcante/claude-conductor/commit/7aa16ed606953ada5fe358156d8e4eeb26e34c25))
* **templates:** Add AskUserQuestion patterns template ([7aa16ed](https://github.com/rbarcante/claude-conductor/commit/7aa16ed606953ada5fe358156d8e4eeb26e34c25))


### Bug Fixes

* Apply black formatting to resolve linting failures ([8562a22](https://github.com/rbarcante/claude-conductor/commit/8562a22a8f82e311f554a11c920f95f015ab1ec0))


### Code Refactoring

* **conductor:** Reduce setup.md token usage by 72% ([#16](https://github.com/rbarcante/claude-conductor/issues/16)) ([7aa16ed](https://github.com/rbarcante/claude-conductor/commit/7aa16ed606953ada5fe358156d8e4eeb26e34c25))
* **agents:** Remove 'conductor:' prefix from agent names ([4cd97f7](https://github.com/rbarcante/claude-conductor/commit/4cd97f75d7d3c92f3f692fc12b4e6f311c23696b))


### Documentation

* Add version badge to README ([75328a5](https://github.com/rbarcante/claude-conductor/commit/75328a5e1cc7dd07e386b53d7ef8a68326012ef5))
* **contributing:** Update conventional commits documentation and version bump rules ([bc8a169](https://github.com/rbarcante/claude-conductor/commit/bc8a169e02a6728056a5a4b674ddc3b75701a192))

## [1.0.1](https://github.com/rbarcante/claude-conductor/compare/v1.0.0...v1.0.1) (2026-01-30)


### Bug Fixes

* **ci:** Sync plugin.json version with releases ([e9f6c0c](https://github.com/rbarcante/claude-conductor/commit/e9f6c0cce9d7224aacc123992aecb7ae1395f1f0))
* **ci:** Sync plugin.json version with releases, remove redundant VERSION file ([5df5eae](https://github.com/rbarcante/claude-conductor/commit/5df5eae4e8815b7bf4e6b67d98a7c2fef439d3c0))

## 1.0.0 (2026-01-30)


### Features

* Add codebase pattern analysis and Progressive Disclosure documentation ([#4](https://github.com/rbarcante/claude-conductor/issues/4)) ([b69b728](https://github.com/rbarcante/claude-conductor/commit/b69b72875d6c8755500dc554e23f3357f48d57d3))
* Add codeReview command for comprehensive code review ([#6](https://github.com/rbarcante/claude-conductor/issues/6)) ([19d6cb4](https://github.com/rbarcante/claude-conductor/commit/19d6cb45bf58befefe44b57d171e72efb8490110))
* **ci:** Add automatic semantic versioning and changelog generation ([f323f11](https://github.com/rbarcante/claude-conductor/commit/f323f114ad4caefbb4bbf32f594a4c3a22d49963))
* **cli:** Add CLAUDE_PLUGIN_ROOT support for plugin file resolution ([4c8d7ae](https://github.com/rbarcante/claude-conductor/commit/4c8d7ae206cf07ce7663a9e6fe15733442e57576))
* **commands:** Add /conductor:skills management command ([c0d1550](https://github.com/rbarcante/claude-conductor/commit/c0d1550048661bf5602950ae28c6683e7f55e1e6))
* **commands:** Add /conductor:snippet command ([93102a7](https://github.com/rbarcante/claude-conductor/commit/93102a773030eef685f7946cf7a64140e5706cd3))
* **commands:** Add Decision Capture protocol to implement.md ([d4a0a7b](https://github.com/rbarcante/claude-conductor/commit/d4a0a7bbb6483276d24017ea8099398aaa09ca01))
* **commands:** Add decisions.md creation to newTrack ([f9ac193](https://github.com/rbarcante/claude-conductor/commit/f9ac193f29dd4b172bb0236eb9b2ee06b98938e9))
* **commands:** Add Git Isolation Protocol for branch enforcement ([#4](https://github.com/rbarcante/claude-conductor/issues/4)) ([a0688fd](https://github.com/rbarcante/claude-conductor/commit/a0688fd2face297d29fe1e40bf96bc8a54e91cfe))
* **conductor:** Add AI Template Generation Protocol ([b6dfd6a](https://github.com/rbarcante/claude-conductor/commit/b6dfd6acf51dbd129fa4202fa3e940c1e97d5df9))
* Implement Universal File Resolution Protocol (UFRP) for feature parity with gemini-cli v0.2.0 ([366d54a](https://github.com/rbarcante/claude-conductor/commit/366d54aabb0edb98c0a79ece5c53b59b0147ee7a))
* **implement:** Add AskUserQuestion to allowed-tools ([43c6489](https://github.com/rbarcante/claude-conductor/commit/43c648980614fca19b6c19cb304ab66d3b687393))
* **implement:** Add CLI command reference for branch suggestions ([ad64b36](https://github.com/rbarcante/claude-conductor/commit/ad64b36d802d0aa54ce4848fcb86182dfaac190b))
* **implement:** Add pattern surfacing step to implement command ([7eb364a](https://github.com/rbarcante/claude-conductor/commit/7eb364a84036be892766a1659137e607418450d4))
* **implement:** Add Section 2.1 GIT ISOLATION SETUP structure ([35f4e8d](https://github.com/rbarcante/claude-conductor/commit/35f4e8d4ab7728a012c11ca34995e064158c9e6c))
* **implement:** Add skill activation step for Phase 5 ([e8d5b93](https://github.com/rbarcante/claude-conductor/commit/e8d5b9326c97e00fb4151bfff5c87205bf6fef1c))
* **implement:** Add Step 1 - Current Branch Detection ([165b8d6](https://github.com/rbarcante/claude-conductor/commit/165b8d6f10d906236ca94e10d9513f717abe38cf))
* **implement:** Add Step 2 - Branch Name Generation ([8b8a935](https://github.com/rbarcante/claude-conductor/commit/8b8a935d8c5ab4c0e20008ecadf6f9d7c365a268))
* **implement:** Add Step 3 - AskUserQuestion Integration ([ae71d72](https://github.com/rbarcante/claude-conductor/commit/ae71d72033947b4ba31741484694d218411c1e58))
* **implement:** Add Step 4 - Git Operations Execution ([8d1a225](https://github.com/rbarcante/claude-conductor/commit/8d1a225674bed0efbcfe883510751a33337ff53e))
* **implement:** Add Step 5 - Error Handling and Fallback ([b9ff020](https://github.com/rbarcante/claude-conductor/commit/b9ff0205e525972e1d9f2e843943f2977a505bcc))
* **implement:** Add suggest-branch subcommand to CLI ([#3](https://github.com/rbarcante/claude-conductor/issues/3)) ([5b2786e](https://github.com/rbarcante/claude-conductor/commit/5b2786eb9818229bd073fb32633ca0ecaaf0ac7c))
* **newTrack:** Add AskUserQuestion tool support for interactive prompts ([de1024d](https://github.com/rbarcante/claude-conductor/commit/de1024da68192e8f6d085f7a8a6e6ea66b70991b))
* **patterns:** Create /conductor:patterns command ([53c14dd](https://github.com/rbarcante/claude-conductor/commit/53c14ddc44f60abd66007035c99055686e1b935e))
* **patterns:** Create configuration pattern ([d42da13](https://github.com/rbarcante/claude-conductor/commit/d42da1379e00eff9ab5735f923c5648b96257450))
* **patterns:** Create error-handling pattern ([5f6b774](https://github.com/rbarcante/claude-conductor/commit/5f6b7745c478d333a43bae8a623a5b0092cd7ceb))
* **patterns:** Create logging pattern ([d8d99f1](https://github.com/rbarcante/claude-conductor/commit/d8d99f1875710af0e71169a5b4a58bf1aa0243f3))
* **patterns:** Create pattern directory structure ([6e69cbd](https://github.com/rbarcante/claude-conductor/commit/6e69cbd3cdeab778f326d6d9105994850aca4fae))
* **patterns:** Create pattern file template ([ab4c97c](https://github.com/rbarcante/claude-conductor/commit/ab4c97c1dd9871af8ba9852eb4258949e75b6dbb))
* **patterns:** Create pattern registry index ([590d150](https://github.com/rbarcante/claude-conductor/commit/590d150b291681af6e4f3d1378a6456190fb2a67))
* **patterns:** Create testing pattern ([e4de867](https://github.com/rbarcante/claude-conductor/commit/e4de8677407bfd4cb78df4fd9533d9cb66185381))
* **patterns:** Create validation pattern ([7ca4c4a](https://github.com/rbarcante/claude-conductor/commit/7ca4c4a9f32a3befc3313bcb7d218496a502f881))
* **patterns:** Design pattern resolution algorithm ([4dffdc0](https://github.com/rbarcante/claude-conductor/commit/4dffdc025007799a874bafa5d1c60591b5d99528))
* **protocol:** Enhance Skill Loading Protocol in CLAUDE.md ([95af186](https://github.com/rbarcante/claude-conductor/commit/95af1867ad169461a5de83c99a62abca4ddbae66))
* **protocols:** Add Decision Capture Protocol ([6fccaee](https://github.com/rbarcante/claude-conductor/commit/6fccaee0f248ba8ca1525ec9e08b356e0f7ae5bf))
* **protocols:** Add Stack Detection Protocol for tech-aware intelligence ([f96e157](https://github.com/rbarcante/claude-conductor/commit/f96e1578b07d77bf23766fb0a27703de550bfbdf))
* **quality:** Add Quality Gate Verification to implement command ([d5d3f36](https://github.com/rbarcante/claude-conductor/commit/d5d3f3636341f5b9dc3fc8b206422bf65706a331))
* **quality:** Add Quality Intelligence section to workflow template ([003a145](https://github.com/rbarcante/claude-conductor/commit/003a1456fe7e473adb1c472fee043e4e5a2f4ab7))
* **quality:** Create anti-pattern directory structure ([881e048](https://github.com/rbarcante/claude-conductor/commit/881e048c6e9e59e3ee21a45674b50d7aad073d6f))
* **quality:** Create anti-pattern file template ([992d6b0](https://github.com/rbarcante/claude-conductor/commit/992d6b0511aa4f8fd19f75dc2ed95d22c9492de8))
* **quality:** Create anti-pattern index ([491520a](https://github.com/rbarcante/claude-conductor/commit/491520af97eef93c8f7bc33150f0e0545ba3eaae))
* **quality:** Create Coverage Intelligence Protocol ([3abcfee](https://github.com/rbarcante/claude-conductor/commit/3abcfee95ae6321ceae1933c7b8062c018ca5efc))
* **quality:** Create deep-nesting anti-pattern ([4edb81a](https://github.com/rbarcante/claude-conductor/commit/4edb81aa844a8ab7754d3d16a4b225730fcc75bc))
* **quality:** Create god-object anti-pattern ([7fd6c15](https://github.com/rbarcante/claude-conductor/commit/7fd6c15bd861200e7b8a1818a089409579275679))
* **quality:** Create magic-numbers anti-pattern ([d25d7ad](https://github.com/rbarcante/claude-conductor/commit/d25d7adea53c5b52bb728cee3d8042a713d138db))
* **quality:** Create mutable-defaults anti-pattern ([914e0c7](https://github.com/rbarcante/claude-conductor/commit/914e0c7834130d9a6ab6b86b0e21828beeeb30bc))
* **quality:** Create Quality Analysis Protocol ([4049441](https://github.com/rbarcante/claude-conductor/commit/404944116c69a6923a41e21c855e97bbb7ae9258))
* **quality:** Create spaghetti-code anti-pattern ([c7be560](https://github.com/rbarcante/claude-conductor/commit/c7be560f90287bde6bf29fca527d9ee8139e13da))
* **scripts:** Add Python CLI for token-efficient conductor operations ([f77d293](https://github.com/rbarcante/claude-conductor/commit/f77d29398176f526538ce6025fe4530fb9f0a8e2))
* **setup:** Add AskUserQuestion tool for structured user interactions ([3dc0e38](https://github.com/rbarcante/claude-conductor/commit/3dc0e380e5422b2b7f137325a1071011655f8d52))
* **setup:** Integrate automatic stack detection for brownfield projects ([cfa4ba7](https://github.com/rbarcante/claude-conductor/commit/cfa4ba73d68bf8f458a4173af08015d13a07020d))
* **skills:** Add api-design reference skill ([1f6c2d7](https://github.com/rbarcante/claude-conductor/commit/1f6c2d7b9b0f0f1d96732c301e2282f5faa1e412))
* **skills:** Add Java best practices skill structure ([51b1d25](https://github.com/rbarcante/claude-conductor/commit/51b1d250ce933764b8cf46195a075d733141802c))
* **skills:** Add Java concurrency content to SKILL.md ([1927d9a](https://github.com/rbarcante/claude-conductor/commit/1927d9a8df7d0f9e1e66c695fa3a01742ce1197c))
* **skills:** Add Java concurrency pattern ([bc45659](https://github.com/rbarcante/claude-conductor/commit/bc456592ebca8a74516beb757d9b3c779d72d3b5))
* **skills:** Add Java modern features content to SKILL.md ([0ae8725](https://github.com/rbarcante/claude-conductor/commit/0ae8725ac8783d9dbe75da747c8675ad00c75374))
* **skills:** Add Java modern-features pattern ([3d4d8c4](https://github.com/rbarcante/claude-conductor/commit/3d4d8c4a3c0c813ad5ba6571b6f4694286ca4cc8))
* **skills:** Add Java SKILL.md core content ([3759fc5](https://github.com/rbarcante/claude-conductor/commit/3759fc577caa66d4f2d392f198276f616425ea4c))
* **skills:** Add Java type-safety pattern ([1f002f5](https://github.com/rbarcante/claude-conductor/commit/1f002f50436fbf81164a4118305239a9d3e8b3f3))
* **skills:** Add java-best-practices to skill registry ([cc8989b](https://github.com/rbarcante/claude-conductor/commit/cc8989beaa4ed4a9f4524aaba247f0370817b68f))
* **skills:** Add JSON schema files for skill validation ([67a33d3](https://github.com/rbarcante/claude-conductor/commit/67a33d3b684b588c5b14761722221ae1ab0b4c5e))
* **skills:** Add reference skills to skill-registry.json ([1c3a8fd](https://github.com/rbarcante/claude-conductor/commit/1c3a8fd2dac6a08d22ef7bb1946250783fe8c67f))
* **skills:** Add Skill Registry System for Phase 3 of Tech Intelligence ([6f4e815](https://github.com/rbarcante/claude-conductor/commit/6f4e8153b21b6203c66c69bda5356e648e9be3a3))
* **skills:** Add testing-strategies reference skill ([c771f3b](https://github.com/rbarcante/claude-conductor/commit/c771f3bf8d2fdbb91b921783d8b7c88f1d38534b))
* **skills:** Add typescript-best-practices reference skill ([f078872](https://github.com/rbarcante/claude-conductor/commit/f0788726d237a886d818b7e097b5c6ab1fac2a33))
* **snippets:** Add Java API client snippet ([7878eb9](https://github.com/rbarcante/claude-conductor/commit/7878eb985c3ed485533314db6bfa8648d4d4d913))
* **snippets:** Add Java dependency injection snippet ([19be31f](https://github.com/rbarcante/claude-conductor/commit/19be31f378d93437b5af391ef92210fddda97108))
* **snippets:** Add Java error handler snippet ([a621d52](https://github.com/rbarcante/claude-conductor/commit/a621d52e5402daf562c7ef9a9e2ef28263bba5c6))
* **snippets:** Add Python and pattern snippet library ([af49af1](https://github.com/rbarcante/claude-conductor/commit/af49af1b2be04e4c931dc3848491946e3c599468))
* **snippets:** Add TypeScript snippet library ([473c46d](https://github.com/rbarcante/claude-conductor/commit/473c46db66e39e26f3c7160873ef9af8703b695a))
* **snippets:** Create snippet library structure and index ([2020fbb](https://github.com/rbarcante/claude-conductor/commit/2020fbb677e4e4e954cc3d9f9694739c52f35bb0))
* **styleguides:** Add AI Quick Reference to general.md ([f10600f](https://github.com/rbarcante/claude-conductor/commit/f10600f0e4c1af90004a178e8bf6c1320f1e2a46))
* **styleguides:** Add AI Quick Reference to go.md ([3b254aa](https://github.com/rbarcante/claude-conductor/commit/3b254aacbd2a141661b6028fe4cbef735a248993))
* **styleguides:** Add AI Quick Reference to javascript.md ([6125bde](https://github.com/rbarcante/claude-conductor/commit/6125bded0464c92f27c9e7d7e962a512f58fa099))
* **styleguides:** Add AI Quick Reference to python.md ([9c0f1a8](https://github.com/rbarcante/claude-conductor/commit/9c0f1a8d1277e320130dcba87ccd430e1cae6e4c))
* **styleguides:** Add AI Quick Reference to typescript.md ([26aa2a3](https://github.com/rbarcante/claude-conductor/commit/26aa2a346c3d302dbb1b82689579958376766e01))
* **templates:** Add Java code styleguide ([62d4566](https://github.com/rbarcante/claude-conductor/commit/62d4566d7c256cc8fee299975505ee121074cdbc))
* **templates:** Create decisions.md ADR template ([c8c3502](https://github.com/rbarcante/claude-conductor/commit/c8c3502d5393fbffce3c6b1b911fb941c0c0672b))
* **templates:** Enhance git notes format with decision references ([f2c4648](https://github.com/rbarcante/claude-conductor/commit/f2c4648a006f1c94719e2a848f8c57806d34cd71))


### Bug Fixes

* Add commit confirmation prompts to newTrack and implement commands ([#5](https://github.com/rbarcante/claude-conductor/issues/5)) ([30fe319](https://github.com/rbarcante/claude-conductor/commit/30fe319f06979b3c0556f1854308bbded7f7296a))
* **newtrack:** Use correct path format in register command ([6674299](https://github.com/rbarcante/claude-conductor/commit/66742993b0ba258d7e7e74a0559200ac71cff050))
* **newtrack:** Use correct path format in register command ([0345ab9](https://github.com/rbarcante/claude-conductor/commit/0345ab93d8ebd19680a033fbdeaa7b83c77c7ee1))
* **patterns:** Add Java and Kotlin file patterns to all core patterns ([20d5155](https://github.com/rbarcante/claude-conductor/commit/20d5155fb6a5706002ccf70fff987e2bb76c1755))
* **setup:** Detect brownfield projects from source code files ([b52e3be](https://github.com/rbarcante/claude-conductor/commit/b52e3bea6931ce44ffae116a6f8c13959380e777))
* **setup:** Detect brownfield projects from source code files ([385302b](https://github.com/rbarcante/claude-conductor/commit/385302bc9e791395b1f53f40675dc9465304e27f))

## [0.1.0](https://github.com/rbarcante/claude-conductor/releases/tag/v0.1.0) - Initial Release

### Features

- Add codeReview command for comprehensive code review
- Add codebase pattern analysis and Progressive Disclosure documentation
- Consolidate CLI context injection across command files
- Add GitHub Actions CI pipeline for Python script testing
- Add Apache 2.0 license compliance notices
- Initial Claude Conductor implementation

### Bug Fixes

- Add commit confirmation prompts to newTrack and implement commands
