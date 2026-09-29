# 1. Executive Summary

## 1.1 Product Identity

**Product Name:** eSub Studio Enterprise — Local Hybrid AI Edition  
**Primary Deployment Target:** Local machine deployment using Streamlit as a single-file `app.py` application  
**Primary AI Runtime Modes:**  
1. **Local LLM mode** via NVIDIA DGX-1-hosted Ollama or OpenAI-compatible local inference gateways  
2. **Cloud API mode** via Gemini API and OpenAI API  
3. **Hybrid failover mode** combining local-first and cloud-selectable execution

This specification defines a redesigned, enterprise-grade, AI-augmented application that preserves all original capabilities while re-architecting the system for **local deployment**, **single-file packaging**, and **hybrid model execution**. The resulting app must support the original functional surface area, the expanded WOW interface system, local/private inference on DGX-1 infrastructure, user-configurable API keys and host IP entry through the web interface, strong UX personalization, live execution visualization, structured note intelligence, agent/skill file handling, notification management, and secure user account management.

## 1.2 Purpose

The app is a multi-functional AI workspace oriented toward structured document workflows, model-assisted note transformation, prompt/skill iteration, workflow execution, and regulated-content review. It must support both general AI productivity scenarios and the higher-rigor structured workflows described in the provided eSub Studio Enterprise specification. The app acts as a unified control plane for:

- Local/private LLM inference hosted on an NVIDIA DGX-1 using Ollama or compatible endpoints
- Gemini API interaction
- OpenAI API interaction
- Future support for Anthropic API and extensible providers
- Prompt, agent, note, and workflow orchestration
- Live logs, token visibility, dashboard-style observability
- Secure operator-facing controls for keys, model routing, and notification preferences

## 1.3 Core Technical Aims

The redesign has eight primary technical aims:

1. **Local-first architecture**  
   Prioritize private inference using DGX-1-hosted local models, especially Gemma-family models served through Ollama or an OpenAI-compatible local endpoint.

2. **Single-file operational packaging**  
   Deliver the user-facing application as a single `app.py` Streamlit app while retaining modular conceptual boundaries internally through disciplined state namespaces, UI sections, configuration layers, and service abstractions.

3. **Feature preservation guarantee**  
   Preserve all original features already described or previously implemented, including dashboard surfaces, note workflows, sidebar functionality, notification system expectations, and account management requirements.

4. **WOW-grade interface modernization**  
   Provide a high-impact visual system with light/dark themes, Traditional Chinese default language, English/Japanese switching, ten Pantone-inspired palette styles, and a “Jackpot” random quick-pick selector.

5. **Transparent execution observability**  
   Add a “WOW visualization” layer for LLM execution, including animated run indicators, live logs, token usage summaries, run-state changes, and interactive dashboard widgets.

6. **Secure secret and endpoint management**  
   Show API key entry fields only if not already sourced from environment variables. Additionally, allow user entry of **host IP / base URL** for local LLM endpoints through the UI.

7. **Extensible model registry**  
   Default to `gemini-3.1-flash-lite`, while enabling user selection of `gemini-3.5-flash-lite`, `gemma-4-31b-it`, `gemma-4-26b-14b-it`, locally registered DGX-served models, and future extensible models.

8. **Operational reliability and blank-screen prevention**  
   The redesign must explicitly prevent common Streamlit blank-screen failure modes through state guards, defensive rendering contracts, schema-backed configuration defaults, progressive loading, and visible error surfaces instead of silent failures.

## 1.4 Major Feature Areas

The specification includes the following major feature families:

- WOW UI/UX personalization
- Local + cloud model orchestration
- LLM execution visualization and live logs
- AI Note Keeper with document ingestion and markdown transformation
- Six AI Magics within Note Keeper
- WOW Sidebar with observability and shortcuts
- Agent/Skill module for `agents.yaml` and `SKILL.md`
- Notification system with user-configurable preferences
- User account management system
- Workflow and dashboard continuity with original features
- Internationalization and future extensibility
- Local deployment architecture for DGX-1 + Ollama + Streamlit

## 1.5 Architectural Position

This version is **not** specified as a Hugging Face Space deployment primary target. Instead, the primary target is **local machine execution**, with the local app connecting outward only when the operator chooses Gemini or OpenAI cloud models. The architecture remains compatible with later packaging for hosted environments, but the baseline assumptions are:

- Local workstation or internal server launches Streamlit
- Local/private model host is operator-configurable
- Secrets may come from environment or interactive UI
- User/session data must be managed securely
- The app remains self-contained as a single-file application artifact

## 1.6 High-Level Design Philosophy

The system must embody the following design philosophy:

- **Local-first, hybrid-capable**
- **Visually premium, operationally transparent**
- **Strictly state-safe**
- **Schema-governed**
- **Extensible by registry, not by hardcoded branching**
- **User-configurable, but policy-constrained**
- **AI-assisted, never silently destructive**
- **Secure by default, explicit by exception**

---

# 2. Functional Specification

## 2.1 UI/UX Options & Flow

### 2.1.1 Global Interaction Model

The application must present a premium, dashboard-driven interface organized into top-level navigation, a collapsible WOW Sidebar, a central workspace region, and contextual status/toolbars. Because the application is implemented as a single Streamlit file, the UI must still emulate a modular enterprise workspace by using clearly segmented panels and state partitions.

The user flow must support two high-level operating patterns:

1. **Direct task execution flow**  
   User selects a feature such as AI Note Keeper, Agent/Skill Module, Fill Agent, Pipeline workspace, or dashboard tools and performs a single focused task.

2. **Workspace continuity flow**  
   User configures theme/language/palette/model/provider/session identity and then moves across modules while preserving session-level state, recent artifacts, logs, and notification context.

### 2.1.2 Primary Navigation Structure

The app must expose the following top-level feature destinations:

- Home / WOW Dashboard
- AI Note Keeper
- Template / Prompt Workspace
- Fill Agent Workspace
- Skill / Agent Workspace
- Pipeline / Workflow Workspace
- Results / Downloads Center
- Notifications Center
- Account / Profile
- Settings / System Preferences
- Diagnostics / Logs / Execution Viewer

If feature consolidation is needed to fit Streamlit ergonomics, these destinations may be represented using tabs, radio selectors, navigation pills, or segmented menus, but the semantic grouping must remain explicit.

### 2.1.3 Default UI State

On first load, the app must initialize with these defaults:

- **Language:** Traditional Chinese (`zh-TW`)
- **Theme:** Light or dark based on user default policy; if no preference exists, default to a sleek dark mode for premium effect or follow prior preference if stored
- **Visual Palette:** First palette in the curated Pantone-inspired set unless Jackpot is invoked
- **Model:** `gemini-3.1-flash-lite`
- **Provider mode:** Cloud Gemini if valid Gemini API key is available; otherwise idle until provider selection/input
- **Sidebar:** Visible
- **WOW visualization pane:** Auto-hidden until a run starts
- **Notification preferences:** All critical/system notifications enabled by default

### 2.1.4 Themes

The app must support at least two high-level themes:

- **Light Theme**
- **Dark Theme**

Each theme must be compatible with all ten visual palette styles. Theme changes must be immediate, session-safe, and non-destructive to current form data or running logs. Theme selection must persist across sessions for authenticated users and optionally for guest/local-only sessions.

### 2.1.5 Language Support

The app must support:

- Traditional Chinese (`zh-TW`) — default
- English (`en`)
- Japanese (`ja`)

All visible UI strings, tooltips, labels, warnings, success messages, and feature descriptions must be routed through a translation layer. User content and model outputs must not be automatically translated unless the user explicitly invokes a translation feature. Logs may preserve raw provider text while UI chrome follows the selected language.

### 2.1.6 Pantone-Inspired Visual Styles

Ten visual styles must be available, each defined by a coherent semantic palette affecting:

- Accent color
- Button emphasis
- Link styling
- Cards/borders
- Token charts and status indicators
- Highlight chips
- Sidebar emphasis tones
- Note keyword highlight options

The style selector must provide:

- Named palette selection
- Preview swatches
- “Jackpot” randomizer that instantly assigns one of the ten styles
- Optional lock behavior to keep current theme while rotating only accent family

The ten palettes should be represented as curated style identities rather than literal Pantone data dependencies, while referencing Pantone-inspired color logic. Each style should specify semantic roles, not raw decorative overrides only.

### 2.1.7 Layout Zones

The UI layout must include:

#### A. Global Header
Contains:
- App identity and logo/title
- Current workspace name
- Language selector
- Theme selector
- Palette selector with Jackpot trigger
- Provider/model quick selector
- Notification icon with unread count
- Account avatar/menu
- Optional compact status signal for active run

#### B. WOW Sidebar
Contains:
- Live log mini-feed
- Token usage visualization
- Quick links
- Notification summary shortcuts
- WOW AI feature launcher cards
- Hide/show toggle
- Session diagnostics badges

#### C. Main Workspace
Contains:
- Module-specific panels
- Forms/editors/uploaders
- Preview areas
- Visualization overlays
- Dashboard cards

#### D. Bottom or floating status rail
Contains:
- Current provider
- Current model
- Run state
- Last sync/save state
- API/environment status indicators

### 2.1.8 Navigation Flow Logic

The app must preserve in-session state when switching modules wherever feasible. The following rules apply:

- Switching between pages/modules must not erase unsaved note content unless the user explicitly resets it.
- File uploads must remain session-bound unless cleared.
- Model and provider selections must remain global unless overridden per module.
- Notifications and logs must be globally accessible from any view.
- If a long-running task is active, the user may navigate away while the task continues and observability remains visible via sidebar/dashboard/notification surfaces.

### 2.1.9 Blank Screen Prevention in UI Flow

To explicitly address blank-screen bugs, the UI contract must guarantee:

- Every module has a minimal safe-state render path, even if dependencies fail
- Missing environment variables result in explicit prompts, not failed renders
- Missing user authentication state falls back to guest mode or auth prompt, not null UI
- Unsupported file input triggers visible error messaging, not broken component states
- Corrupt or absent session keys are auto-reinitialized
- Visualization components render placeholders when no run exists
- All selectors have defaults
- Every dynamic pane must degrade to a text status card instead of rendering nothing

### 2.1.10 Accessibility and Interaction Quality

The interface should support:

- High-contrast compatibility within both themes
- Keyboard-accessible navigation where Streamlit constraints allow
- Clear selection states
- Non-color-only status encoding
- Animation with graceful fallback for reduced-motion preferences
- Readable typography for mixed-language content

---

## 2.2 Visualization

### 2.2.1 Purpose

The “WOW visualization” layer is a dedicated observability subsystem designed to make AI execution legible, animated, and interactive. It must help users understand:

- What the LLM is doing now
- Which provider/model is active
- Whether tokens are increasing
- Which step just completed
- What artifacts were produced
- Whether warnings/errors occurred
- How long the execution has been running

### 2.2.2 LLM Execution Indicator

An animated execution indicator must appear whenever a run is active. It should convey:

- Idle
- Queued
- Connecting
- Sending request
- Streaming response
- Post-processing
- Completed
- Warning
- Error
- Blocked / configuration needed

The indicator may appear in:
- Header status badge
- Main visualization pane
- Sidebar compact widget

The animation must remain informative rather than ornamental. It should reflect actual state transitions derived from run lifecycle events.

### 2.2.3 Live Log Design

The live log system must support three display modes:

1. **Compact Sidebar Feed**
   - Most recent events only
   - Time-stamped
   - Severity-coded
   - Click to expand

2. **Expanded Run Log Viewer**
   - Full chronological log
   - Filter by run ID, module, provider, severity
   - Copy/export text
   - Search within log
   - Show hidden technical details only on demand

3. **Structured Event Timeline**
   - Step cards or milestone progression
   - Indicates start/end/duration
   - Shows retries and provider routing decisions
   - Highlights user actions versus system actions

Log event categories must include:
- UI
- Auth
- Notifications
- File ingest
- Parsing
- Provider connectivity
- Model inference
- Validation
- Export/download
- Error/recovery
- System update

### 2.2.4 Dashboard Interactions

The WOW dashboard must provide interactive cards or charts for:

- Total runs this session
- Current active run duration
- Provider distribution
- Token usage estimates
- Success/failure/warning ratios
- Uploaded artifact counts
- Notes processed count
- Agent/skill import counts
- Notification counts by category
- Recent outputs

Widgets should be clickable to filter logs or navigate to related modules.

### 2.2.5 Run State Visibility

Each run must expose at minimum:
- Run ID
- Start time
- Initiating module
- Provider
- Model
- Prompt/input source type
- Token estimates if available
- Status
- Output artifact type
- Errors/warnings if any

### 2.2.6 Token Usage Visualization

Because providers differ in what usage details they return, the token visualization system must support:
- Exact counts when available
- Estimated counts when exact counts unavailable
- Clear distinction between exact and estimated
- Input vs output token split
- Session aggregate
- Optional cost estimate for cloud models
- Zero-cost/local indicator for private runs where monetary cost is not computed

### 2.2.7 Visualization in Long-Running Tasks

Long-running operations such as note transformation, PDF extraction, pipeline execution, comparison runs, or batch model evaluation must display:
- Progress stage labels
- Approximate elapsed time
- Last completed step
- Current step description
- Retry indicator if applicable
- Completion notification on finish

### 2.2.8 Visualization Failure Safety

If event streaming or internal state updates fail:
- The system must fall back to periodic status refresh
- The UI must show “live updates degraded” rather than go blank
- Logs must remain readable from last known state
- Completion state must still generate a notification if determinable

---

## 2.3 API/Model Management

### 2.3.1 Supported Providers

The provider abstraction must support:
- **Gemini API**
- **OpenAI API**
- **Local LLM via Ollama**
- **Local OpenAI-compatible endpoint** hosted on DGX-1 or another internal gateway
- **Future provider slot** for Anthropic API and other extensible providers

### 2.3.2 User Input Requirements

The UI must allow user entry of:
- Gemini API key
- OpenAI API key
- Local host IP / base URL for DGX-1-hosted LLM
- Optional local provider alias/name
- Optional local authentication token if later required
- Optional timeout override
- Optional connectivity test trigger

### 2.3.3 Environment Precedence Rules

API key field visibility must obey the following logic:

1. On startup, inspect relevant environment variables.
2. If a provider key exists in environment:
   - Do not display its input field
   - Do not display its value
   - Show only a masked status badge such as “Gemini key available from environment”
3. If the key does not exist in environment:
   - Show the relevant input field
   - Do not persist secret values insecurely
4. If a user enters a key during session:
   - Store only in volatile session memory unless explicit secure local persistence policy exists
5. The local host/base URL field is always allowed, because endpoint selection is operational, not a secret by default, though it may be masked if enterprise policy requires

### 2.3.4 Concealment Rules

The app must never:
- Echo raw secrets in logs
- Display full keys after entry
- Include secret values in downloadable configs
- Persist secrets in plain text local storage

If secure persistence is supported for logged-in users, it must use encryption-at-rest or secure OS-backed storage abstraction. If not available, secrets remain session-only.

### 2.3.5 Provider Selection UX

Provider selection must be separated from model selection. The UI should support:
- Provider dropdown/radio
- Model dropdown filtered by provider
- Manual custom model text field when “custom” is enabled
- Connection status indicator per provider
- Test connection action
- Current routing mode display

### 2.3.6 Default Model

The global default model must be:
- `gemini-3.1-flash-lite`

### 2.3.7 Required Selectable Models

The selector must initially include:
- `gemini-3.1-flash-lite`
- `gemini-3.5-flash-lite`
- `gemma-4-31b-it`
- `gemma-4-26b-14b-it`

Additionally, it must support:
- Other Ollama-listed local models discovered from host
- Other OpenAI-compatible model IDs returned by local endpoint
- Future cloud models added via registry
- Manual user-defined custom model entry

### 2.3.8 Local Model Discovery

If the local provider supports discovery, the app should query the local endpoint for available models. If discovery is not available:
- Allow manual model entry
- Cache successful model IDs for session reuse
- Distinguish discovered vs user-defined models

### 2.3.9 Routing Modes

The app should support the following routing modes:
- **Manual provider + manual model**
- **Local-first fallback-to-cloud**
- **Cloud-first fallback-to-local**
- **Module override mode**
- **Run-specific explicit lock mode**

### 2.3.10 Connectivity Validation

Connectivity validation must test:
- Endpoint syntactic validity
- Reachability
- Authentication sufficiency if applicable
- Model availability
- Response format compatibility
- Timeout behavior

The result must surface as:
- PASS / WARN / FAIL
- Human-readable issue summary
- Suggested remediation

### 2.3.11 Model Capability Metadata

The registry for each model should track:
- Provider
- Model ID
- Supports chat/text generation
- Supports long context
- Supports structured output preference
- Supports streaming
- Supports local/private execution
- Performance tier
- Cost tier if cloud
- Status (active, experimental, deprecated)

### 2.3.12 Failure Rules

If the user selects an unavailable model:
- The app must explicitly show model-not-found or endpoint mismatch
- It must not silently substitute another model
- It may suggest alternatives, but substitution requires user confirmation

---

## 2.4 AI Note Keeper

### 2.4.1 Purpose

AI Note Keeper is a structured note ingestion, transformation, editing, and enrichment workspace. Users may paste or upload raw material and convert it into organized markdown that is easier to review, edit, export, and annotate.

### 2.4.2 Supported Input Types

The module must support:
- Plain text
- Markdown
- PDF
- Drag-and-drop or file picker upload
- Direct paste
- Optional multi-document note ingestion in future mode

### 2.4.3 Ingestion Workflow

The transformation workflow must include:
1. Input acquisition
2. File type detection
3. Size/basic validation
4. PDF text extraction if applicable
5. Text normalization
6. Structure inference
7. Organized markdown generation
8. Keyword extraction/highlight overlay
9. User review/edit
10. Optional AI Magic enhancement

### 2.4.4 Organized Markdown Output Contract

Transformed notes must be converted into organized markdown using a consistent output structure where possible:
- Title section
- Summary block
- Main topic headings
- Bullet or numbered points
- Action items section if detected
- References or source notes section if relevant
- Preserved quotations if present

The system should avoid over-inventing structure when the input is sparse. Minimal content should remain minimal but cleanly formatted.

### 2.4.5 Coral Keyword Highlighting

“Important keywords” must be rendered in a **coral-colored emphasis style** in markdown preview. Because raw markdown does not natively define color, the implementation contract should treat coral highlighting as a rendering-layer annotation, not a lossy textual mutation. The system must maintain:
- Underlying plain markdown-safe content
- Visual highlight metadata
- Export compatibility strategy

If export is markdown-only, the highlights may be represented via inline markup conventions or metadata-compatible formatting rules. In plain-text mode, highlights are represented as textual markers or omitted from visual coloration while preserving keyword tags.

### 2.4.6 Editing Modes

The module must provide:
- **Markdown view/edit mode**
- **Plain text view/edit mode**
- **Rendered preview mode**
- Optional split-pane edit/preview mode

Mode switching must not destroy formatting. A canonical internal note representation should preserve both textual content and optional highlight metadata.

### 2.4.7 PDF Handling

For PDF input:
- Extract text if available
- If extraction is poor or empty, show a warning
- Allow user to proceed, retry, or mark the result as incomplete
- Preserve page-level segmentation if useful for later AI Magics
- Record source metadata for traceability

### 2.4.8 Output Persistence

Users must be able to:
- Keep notes in current session
- Download as markdown
- Download as text
- Copy to clipboard
- Re-run transformation with a different model
- Apply AI Magic tools iteratively

### 2.4.9 Error Handling

If note transformation fails:
- Preserve original input
- Show stage-specific error information
- Offer retry
- Offer switch-model or switch-provider suggestion
- Keep partial extracted text if available

---

## 2.5 AI Magics & WOW AI Features

### 2.5.1 AI Magics Overview

AI Note Keeper must include at least six AI-powered features branded as **AI Magics**. These features operate primarily on notes and note-derived content.

#### AI Magic #1: AI Keywords
**Description:** User inputs keywords and selects one or more highlight colors; system detects, tags, and visually highlights those keywords across the note.  
**Functional details:**
- User can enter custom keywords manually
- User can paste comma-separated keyword sets
- User selects highlight color(s)
- Coral remains default recommended emphasis color
- Supports exact match and optional fuzzy/variant match mode
- Can combine user-defined and AI-suggested keyword lists
**Rationale:** Improves rapid scanning, semantic grouping, and review efficiency.

#### AI Magic #2: Smart Summarizer
**Description:** Generates layered summaries from notes: short, medium, and detailed versions.  
**Functional details:**
- Short summary for dashboard card
- Medium summary for reading
- Detailed summary retaining section references
- Language output follows selected UI language unless user overrides
**Rationale:** Supports executive overview and deep review without reprocessing source every time.

#### AI Magic #3: Structure Refiner
**Description:** Reorganizes messy notes into clearer headings, bullets, action items, decisions, and open questions.  
**Functional details:**
- Can preserve original sequence or optimize for logical grouping
- Flags uncertain structural decisions
- Preserves quotations
**Rationale:** Converts raw capture into usable working knowledge.

#### AI Magic #4: Action Extractor
**Description:** Detects tasks, deadlines, owners, and follow-up items from notes.  
**Functional details:**
- Creates action list block
- Uses confidence tagging for inferred owners/dates
- Allows manual confirmation before committing action tags
**Rationale:** Makes note output immediately operational.

#### AI Magic #5: Terminology Explainer
**Description:** Detects specialized terms and provides concise in-context explanations.  
**Functional details:**
- Hover or expandable glossary entries
- Multi-language explanation support
- Can limit to domain-critical terms only
**Rationale:** Enhances cross-functional collaboration and understanding.

#### AI Magic #6: Rewrite Lens
**Description:** Rewrites selected note portions into alternative styles such as formal, concise, bilingual draft, meeting minutes, or action memo.  
**Functional details:**
- Selection-based operation
- Output inserted as proposal or alternate pane
- Original text always preserved
**Rationale:** Speeds repurposing of notes for multiple downstream uses.

### 2.5.2 WOW AI Features Overview

In addition to AI Magics, the app must include WOW AI features spanning the broader platform. At minimum, three of these must appear in the WOW Sidebar, and three more must be newly introduced beyond the original brief. This specification defines ten total WOW AI features for platform-wide use.

#### WOW AI #1: Live Execution Pulse
A visual and semantic run monitor that shows current LLM phase, elapsed time, provider, model, recent tokens, and last event.

#### WOW AI #2: Token Budget Sentinel
Tracks token and cost/compute consumption across runs; warns of approaching session budgets and highlights expensive operations.

#### WOW AI #3: Quick Route Genius
Suggests the best feature entry point or model/provider based on the user’s uploaded content and task intent.

#### WOW AI #4: Consistency Cross-Checker
Cross-checks structured or note-derived content for contradictions, duplications, mismatches, and revision drift.

#### WOW AI #5: Template Migration Assistant
Maps content from one template or structure version into another, highlighting uncertain mappings.

#### WOW AI #6: Public Release Redaction Assistant
Identifies sensitive text for review and redaction proposals in user documents or notes.

#### WOW AI #7: Prompt Comparator
Lets users compare two prompt/model setups on the same input and review output differences side-by-side.

#### WOW AI #8: Source-to-Claim Traceboard
Builds traceability from generated statements back to source snippets when source-bearing inputs exist.

#### WOW AI #9: Session Recovery Oracle
Analyzes app/session state and helps recover incomplete work after interruptions, reloads, or provider failures.

#### WOW AI #10: Insight Burst
Provides context-aware suggestions such as “summarize this,” “extract actions,” “compare two versions,” or “convert to skill template” based on active content.

### 2.5.3 In-Depth Rationale for AI Magics and WOW AI Features

The AI Magics are note-centric and optimized for transforming raw content into structured knowledge assets. The WOW AI features are platform-centric and optimized for making the application feel proactive, observable, and operationally intelligent. Their separation prevents feature sprawl while preserving clear mental models for users and AI coding assistants implementing the system.

### 2.5.4 Proposal-Not-Overwrite Rule

Any AI transformation that materially rewrites content should be surfaced as:
- Replace current
- Insert below
- Open side-by-side comparison
- Apply selected changes only

This prevents silent destructive overwrites, especially relevant for notes, templates, or skill files.

---

## 2.6 WOW Sidebar

### 2.6.1 Purpose

The WOW Sidebar is a persistent, collapsible, high-value contextual control rail.

### 2.6.2 Required Elements

The sidebar must include:
- Live log mini-feed
- Token usage mini visualization
- Quick links to major features
- Hide/show toggle
- Notification preview
- Active run summary
- Provider/model status
- Three WOW AI quick-launch actions
- Recent artifacts list
- Session health indicators

### 2.6.3 Display Logic

The sidebar must support:
- Expanded mode
- Collapsed icon mode
- Auto-focus highlight when a new notification arrives
- Context-sensitive panels depending on current module
- Sticky state persistence per session/user

### 2.6.4 Interactivity

Users must be able to:
- Click log items to open full run viewer
- Click token widget to open detailed usage pane
- Launch AI Magics or WOW AI actions
- Jump to Notes, Skill, Dashboard, or Settings
- Dismiss informational cards
- Expand/collapse sections individually

### 2.6.5 Additional Three WOW AI Sidebar Features

The three specifically emphasized sidebar WOW AI additions are:

1. **Quick Route Genius**  
   Suggests where in the app the user should go next based on current content and configuration.

2. **Session Recovery Oracle**  
   Detects interrupted tasks or incomplete content flows and offers resume actions.

3. **Insight Burst**  
   Surfaces one-click AI actions inferred from the current context.

These are deliberately chosen because they add high utility to the sidebar’s always-available nature.

### 2.6.6 Token Visualization Rules

The sidebar token display must show:
- Current run token count or estimate
- Session total
- Cloud cost estimate if available
- Local run compute indicator if no monetary estimate
- Warning if usage spikes unexpectedly

### 2.6.7 Integration with Notifications

The sidebar must display:
- Recent unread count
- Notification type badges
- Shortcut into preferences
- “Mute temporarily” quick action
- Task completion banners for long-running operations

---

## 2.7 Agent/Skill Module

### 2.7.1 Scope

The module must allow users to:
- Paste/upload/download/modify `agents.yaml`
- Paste/upload/download/modify `SKILL.md` or `skill.md`
- Standardize pasted/uploaded `agents.yaml` prior to import
- Validate and format content
- Preserve all original file-editing capability

### 2.7.2 Supported Actions

For both agents and skills:
- Create new
- Paste content
- Upload file
- Validate
- Standardize/format
- Edit in text area
- Download normalized file
- Compare original vs standardized result
- Reset working copy
- Save to session or user workspace

### 2.7.3 agents.yaml Validation and Standardization

The system must perform a validation pipeline for `agents.yaml`:
1. Parse as YAML
2. Detect syntax errors
3. Validate required top-level structure
4. Normalize ordering and whitespace
5. Ensure list/map consistency
6. Detect duplicate keys where parser surfaces them
7. Produce standardized YAML output
8. Surface warnings for non-blocking issues

Standardization should aim for:
- Stable formatting
- Predictable indentation
- Canonical key ordering where applicable
- Preservation of comments only if implementation supports it; otherwise warn user comments may be lost during normalization

### 2.7.4 SKILL.md Handling

For `SKILL.md`, the module must support:
- Raw markdown editing
- Optional frontmatter detection
- Frontmatter validation if present
- Separation of metadata and body in preview
- Download as `.md`

### 2.7.5 Import Rules

Importing standardized content into an active workspace must require explicit confirmation. The app must distinguish between:
- **Preview standardized**
- **Use standardized**
- **Keep original**
- **Discard import**

### 2.7.6 Error Handling

If a YAML parse fails:
- Preserve raw pasted/uploaded text
- Show structured error summary with line/column if available
- Offer formatting guidance
- Do not wipe user content

### 2.7.7 Future Extensibility

The validation pipeline must be designed so future schemas for:
- agents manifests
- skills registries
- pipeline files
- prompt packs
can be added without redesigning the module shell.

---

## 2.8 User Account Management System

### 2.8.1 Purpose

The application must include a user account system supporting:
- Registration
- Login
- Logout
- Password reset
- Profile management
- Secure storage expectations
- Local deployment compatibility

### 2.8.2 Modes

Two modes must be supported:

1. **Guest / Local Session Mode**
   - No persistent account required
   - Useful for personal local workflows
   - Some preferences stored session-only or local-safe storage

2. **Authenticated User Mode**
   - Registration and login enabled
   - Profile persistence
   - Notification preferences persistence
   - Saved work history and personalization

### 2.8.3 Registration Fields

At minimum:
- Username or email
- Password
- Confirm password
- Display name
- Optional organization/team
- Optional role/title
- Language preference
- Theme preference

### 2.8.4 Security Requirements

User data must be stored securely. The specification requires:
- Passwords must never be stored in plaintext
- Strong hashing with per-user salt
- Optional local encrypted file/database storage
- Secure reset workflow
- Session invalidation on logout
- No secret leakage in logs

### 2.8.5 Password Reset

Password reset must support:
- User identity submission
- Verification flow appropriate to local deployment context
- Secure password update
- Reset result notification
- Rate-limiting or cooldown consideration

### 2.8.6 Profile Management

Users must be able to update:
- Display name
- Email if allowed by policy
- Organization/team
- Role/title
- Preferred language
- Preferred theme/palette
- Notification preferences
- Optional saved provider defaults excluding hidden environment-managed secrets

### 2.8.7 Storage Options

Because this is a local deployment single-file app, storage implementation may use:
- Local file-based database
- Embedded database
- External internal DB if configured

The specification requires the storage layer to be abstract enough that secure persistence can later migrate without UI redesign.

### 2.8.8 Authentication Failure UX

On auth errors:
- Show explicit message
- Never disclose whether password or account was specifically incorrect if policy forbids
- Never crash UI
- Preserve partially entered non-secret form fields when reasonable

---

## 2.9 Notification System

### 2.9.1 Purpose

The app must include a notification system for significant events such as:
- Completion of long-running tasks
- Pipeline execution milestones
- New feature releases
- Important system updates
- Connectivity issues
- Validation failures
- Security-relevant warnings
- Account actions

### 2.9.2 Notification Categories

At minimum:
- Task
- Pipeline
- Feature release
- System update
- Security
- Account
- Reminder
- Success
- Warning
- Error

### 2.9.3 Delivery Surfaces

Notifications must appear through:
- Header bell center
- Sidebar summary
- Toast popups
- Optional module-local banners
- Persistent notifications panel/history

### 2.9.4 Notification Preferences

Users must be able to configure:
- Which categories are enabled
- Toast on/off
- Sound on/off if implemented
- Duration of transient popups
- Do-not-disturb windows
- Only critical alerts mode
- Session-only mute

### 2.9.5 Notification Payload Model

Each notification should include:
- Unique ID
- Category
- Severity
- Timestamp
- Title
- Message
- Related module
- Related run or artifact ID if applicable
- Read/unread state
- Action link if applicable
- Expiration/archive policy

### 2.9.6 Long-Running Task Alerts

When a long task completes:
- Mark success/failure/warning clearly
- Include task name and run context
- Provide jump link to results/logs
- Respect preferences but always surface critical failures

### 2.9.7 Feature Release and System Update Notifications

These notifications must support:
- Dismiss once
- View details
- “What changed” summaries
- Optional pinning until seen
- Localization

### 2.9.8 Reliability Contract

Notification generation must be best-effort but robust:
- If toasts fail, notification center still records events
- If UI refresh occurs, persisted notification history remains if logged-in mode supports it
- Critical events should attempt duplication in multiple surfaces

---

## 2.10 Extensibility & Internationalization

### 2.10.1 Extensible Model Registry

The app must not hardcode a closed list of models. Instead it must expose:
- Seeded default registry
- Provider-scoped discovery
- Manual additions
- Metadata-backed capabilities

### 2.10.2 Future Language Expansion

The i18n architecture must support:
- Additional locale packs without redesign
- Fallback chain behavior
- Key-based translation consistency
- Language-specific formatting for timestamps and labels

### 2.10.3 Translation Governance

UI translations should be separated from:
- User content
- Model outputs
- Logs
- Imported files

Only interface strings must change automatically on locale switch.

### 2.10.4 Theme/Palette Expansion

The design token system must support:
- New palettes
- Enterprise branding overrides
- Accessibility variants
- Reduced-motion modes

### 2.10.5 Feature Registration

New modules or WOW AI features should be registerable by:
- ID
- title by locale
- description by locale
- route/view type
- icon/meta
- provider dependency requirements
- beta/stable flag

### 2.10.6 File Format Growth

The ingestion framework should be adaptable to:
- DOCX
- HTML
- CSV
- JSON notes
- ZIP packages
without breaking current flows.

---

## 2.11 Deployment & Hosting

### 2.11.1 Primary Deployment Target

This specification defines deployment on a **local machine** using:
- Streamlit
- Single file `app.py`
- Optional local embedded storage
- Browser-based access on local network or localhost
- Connectivity to DGX-1-hosted local LLM endpoints

### 2.11.2 Local LLM Hosting Assumption

The local private LLM environment is assumed to run on:
- NVIDIA DGX-1
- Ollama-serving Gemma-family models
- Possibly OpenAI-compatible local serving layer
- Operator-specified host IP or base URL

The app must allow the user to input the local host connection in the web UI.

### 2.11.3 Single app.py Constraint

All user-visible application logic is delivered in a single `app.py`.  
This constraint changes packaging but must not collapse architecture quality. The specification therefore requires conceptual modularity through:
- Named state domains
- Feature-scoped rendering functions or sections
- Provider/service registries
- Shared validation contracts
- Configuration namespaces
- Uniform event/notification models

### 2.11.4 API Support

The application must support:
- Gemini API
- OpenAI API
- Local Ollama endpoint
- Local OpenAI-compatible endpoint
- Future Anthropic API support via extensible provider design

### 2.11.5 Environmental Variable Guidelines

Environment variables are allowed for:
- Gemini API key
- OpenAI API key
- Optional default local host/base URL
- Optional app secret for local encryption/session signing
- Optional default language/theme
- Optional user store configuration

Visibility rules:
- If secret exists in environment, UI must not show editable secret field
- Instead, show availability status only
- Non-secret operational fields like host/base URL may remain editable depending on policy

### 2.11.6 Local Security Posture

Because deployment is local, the app must still consider:
- Shared workstation risk
- Network-exposed Streamlit instances
- Session hijacking risk on LAN
- Secret persistence risk
- Local file permission issues
- Download/export confidentiality

### 2.11.7 Operational Modes

The app should support:
- Localhost single-user mode
- Local network team demo mode
- Internal secured workstation mode
- Semi-persistent departmental mode with account system enabled

### 2.11.8 Diagnostics and Startup Checks

On startup the app should perform safe diagnostics:
- Environment variable discovery
- Storage availability
- Provider configuration presence
- Translation pack integrity
- Theme configuration sanity
- Optional local endpoint reachability test

Failures must appear as visible warnings, never as a blank page.

---

# 3. Tables

## 3.1 Design Decisions Table

| Decision | Brief Spec | Rationale |
|---|---|---|
| Local-first deployment | Primary runtime is a local Streamlit app on workstation/server, not hosted-first | Aligns with DGX-1 private inference and enterprise data-control needs |
| Single-file app shell | Deliver as single `app.py` while preserving internal conceptual modularity | Satisfies deployment simplicity without sacrificing architecture clarity |
| Hybrid provider gateway | Gemini, OpenAI, Ollama, and OpenAI-compatible local endpoints share one provider abstraction | Reduces branching complexity and enables future extensibility |
| Default model policy | Global default is `gemini-3.1-flash-lite` | Matches requested baseline and balances speed with usability |
| Explicit model registry | Seed fixed models plus provider discovery and manual custom model support | Prevents future lock-in and supports evolving local inventories |
| Hidden environment secrets | API key fields never display if sourced from environment | Improves security and satisfies requirement for concealment rules |
| User-entered local host | Local host IP/base URL is configurable through UI | Critical for DGX-1 and operational flexibility across internal networks |
| WOW observability layer | All runs emit structured lifecycle events visible in dashboard and sidebar | Eliminates opaque AI behavior and improves trust/debuggability |
| Blank-screen fail-safe rendering | Every dynamic view has a safe fallback state and default initialization | Prevents silent Streamlit rendering failures |
| State namespace isolation | Session state segmented by auth, notes, provider, logs, notifications, artifacts, UI | Minimizes cross-feature corruption in a single-file architecture |
| Two-tier editing for notes | Markdown and plain-text modes share canonical representation with highlight metadata | Preserves usability and avoids destructive format switching |
| Coral-highlight rendering model | Important keywords are rendered coral visually while underlying content stays portable | Meets requirement without corrupting markdown interoperability |
| YAML standardization before import | `agents.yaml` is parsed, validated, normalized, previewed, then imported on confirmation | Protects workspace integrity and improves consistency |
| Notification preference engine | Category-level and surface-level notification controls are user-configurable | Supports professional workflows and reduces alert fatigue |
| Guest + account dual mode | Supports immediate local use plus persistent accounts for enterprise continuity | Balances frictionless access with secure personalization |
| Non-silent model failure rule | Unavailable model IDs must error explicitly with no stealth substitution | Preserves transparency and user trust |
| Token telemetry with estimate mode | When providers do not return exact usage, estimates are shown and labeled | Maintains observability across heterogeneous providers |
| WOW Sidebar as command rail | Sidebar combines logs, token summary, quick links, and AI shortcuts | Concentrates high-frequency controls in one persistent location |
| Translation-first UI strings | All chrome text is locale-driven; user data remains untranslated unless requested | Ensures safe multilingual support without data mutation |
| Extensible feature registration | New modules, models, languages, and WOW features attach by metadata contract | Future-proofs the app and helps AI coding tools extend it reliably |

## 3.2 WOW AI Features Table

| Feature Title | Brief Spec | Comments |
|---|---|---|
| Live Execution Pulse | Animated run-state monitor with provider/model/status/timing visibility | Core WOW visualization anchor |
| Token Budget Sentinel | Tracks tokens, estimates cost, flags budget or compute spikes | Especially useful across cloud vs local modes |
| Quick Route Genius | Suggests best module, provider, or next step from current user context | Strong UX accelerator in multi-feature apps |
| Consistency Cross-Checker | Detects contradictions across notes, templates, or outputs | Valuable for regulated or structured documentation |
| Template Migration Assistant | Maps old structures into new template formats with confidence markers | High long-term utility for evolving workflows |
| Public Release Redaction Assistant | Suggests redactions for sensitive content before sharing/export | Useful for governance and safe collaboration |
| Prompt Comparator | Compares two settings/prompts/models on identical input | Bridges experimentation and operational use |
| Source-to-Claim Traceboard | Shows evidence/source links behind generated outputs when source text exists | Improves trust and reviewability |
| Session Recovery Oracle | Detects interrupted sessions and proposes recovery/resume actions | Directly addresses reliability and blank-screen aftermaths |
| Insight Burst | Surfaces context-aware one-click AI actions in sidebar and dashboard | Makes app feel proactive and intelligent |

---

# 4. Quality Evaluations

## 4.1 Evaluation Method Framing

The following ten quality evaluations are defined as pass/fail gates for the redesigned specification. Each criterion includes explicit logic and a compact stepwise determination trail. Summary results are shown only if all ten criteria pass.

---

### Evaluation 1: Requirement Coverage Completeness

**Criterion definition:**  
The specification must cover all explicitly requested capabilities: local deployment, single `app.py`, local DGX-1/Ollama support, Gemini/OpenAI support, UI entry for API keys and host IP, default model policy, model selector extensibility, preservation of original features, WOW UI, Note Keeper, Agent/Skill module, sidebar, tables, evaluations, follow-up questions, and deployment/security/internationalization notes.

**Evaluation logic/conditions:**
1. Check whether deployment target is local machine rather than hosted-only.
2. Check whether single-file `app.py` packaging is specified.
3. Check whether local LLM host IP/base URL input is specified.
4. Check whether Gemini and OpenAI APIs are included.
5. Check whether required model list is included.
6. Check whether original features and expanded modules are preserved.
7. Check whether required output sections exist.

**Stepwise determination:**
- Local deployment target is explicitly defined in Sections 1 and 2.11.
- Single-file `app.py` constraint is explicitly handled in Section 2.11.3.
- Host IP/base URL user input is specified in Section 2.3.2.
- Gemini and OpenAI support are specified in Sections 2.3.1 and 2.11.4.
- Required models are defined in Section 2.3.7.
- Note Keeper, WOW Sidebar, Agent/Skill module, notifications, and accounts are specified.
- Tables, evaluations, follow-up questions, and appendix are present in the document structure.

**Determination:** PASS

---

### Evaluation 2: Deployment Feasibility for Local DGX-1 Hybrid Use

**Criterion definition:**  
The specification must be implementable on a local machine that connects to a DGX-1-hosted local model service while also allowing cloud APIs.

**Evaluation logic/conditions:**
1. Verify local endpoint connectivity assumptions are present.
2. Verify cloud provider coexistence is supported.
3. Verify model routing and selection are not hardcoded to one provider.
4. Verify the local host can be changed by the user.

**Stepwise determination:**
- DGX-1-hosted Ollama/local endpoint assumptions are described in Sections 1.2, 2.3, and 2.11.
- Gemini and OpenAI remain selectable in the same provider framework.
- Routing modes include local-first and cloud-first strategies.
- The UI accepts local host/base URL values from the user.

**Determination:** PASS

---

### Evaluation 3: Security and Secret Handling Adequacy

**Criterion definition:**  
Secrets and credentials must be handled with explicit concealment rules and safe storage expectations.

**Evaluation logic/conditions:**
1. Environment-managed secrets must be hidden from UI.
2. User-entered secrets must not be logged.
3. Plaintext persistence must be disallowed or tightly constrained.
4. Account/password handling must require secure storage language.

**Stepwise determination:**
- Environment precedence and concealment rules are defined in Section 2.3.3 and 2.3.4.
- Logging restrictions for secrets are explicitly stated.
- Persistence is limited to volatile session or secure storage expectations.
- Password security requirements are defined in Section 2.8.4.

**Determination:** PASS

---

### Evaluation 4: UX Personalization Completeness

**Criterion definition:**  
The WOW interface must include themes, three languages, ten palette styles, and a Jackpot selector.

**Evaluation logic/conditions:**
1. Confirm light/dark theme support.
2. Confirm Traditional Chinese default plus English and Japanese.
3. Confirm ten visual styles.
4. Confirm Jackpot quick-pick behavior.

**Stepwise determination:**
- Theme support is specified in Section 2.1.4.
- Language defaults and options are defined in Section 2.1.5.
- Ten palette styles are defined in Section 2.1.6.
- Jackpot selector behavior is explicitly included in Section 2.1.6.

**Determination:** PASS

---

### Evaluation 5: Observability and Live Visualization Adequacy

**Criterion definition:**  
The app must provide meaningful execution observability for LLM activity.

**Evaluation logic/conditions:**
1. Check for animated execution indicator.
2. Check for live log system.
3. Check for dashboard metrics/widgets.
4. Check for token usage visibility.
5. Check for failure/degraded-state handling.

**Stepwise determination:**
- Animated LLM execution indicator is defined in Section 2.2.2.
- Live logs appear in sidebar, expanded viewer, and event timeline forms.
- Dashboard interaction cards are defined in Section 2.2.4.
- Token usage visualization rules are specified in Sections 2.2.6 and 2.6.6.
- Degraded visualization fallback behavior is specified in Section 2.2.8.

**Determination:** PASS

---

### Evaluation 6: AI Note Keeper Completeness

**Criterion definition:**  
AI Note Keeper must satisfy file input, markdown transformation, coral keyword highlighting, edit modes, and AI Magics requirements.

**Evaluation logic/conditions:**
1. Confirm text/markdown/PDF support.
2. Confirm transformation into organized markdown.
3. Confirm coral keyword handling.
4. Confirm markdown/plain-text editing.
5. Confirm at least six AI Magics are defined.

**Stepwise determination:**
- Supported file types are defined in Section 2.4.2.
- Transformation workflow and output structure are specified in Sections 2.4.3 and 2.4.4.
- Coral rendering rules are defined in Section 2.4.5.
- Editing modes are specified in Section 2.4.6.
- Six AI Magics are defined in Section 2.5.1.

**Determination:** PASS

---

### Evaluation 7: Agent/Skill Module Precision

**Criterion definition:**  
The spec must clearly define actions and standardization/validation behavior for `agents.yaml` and `SKILL.md`.

**Evaluation logic/conditions:**
1. Confirm paste/upload/download/modify support.
2. Confirm YAML validation before import.
3. Confirm standardization rules.
4. Confirm skill markdown handling.
5. Confirm error preservation behavior.

**Stepwise determination:**
- Required actions are listed in Section 2.7.2.
- Validation pipeline is defined in Section 2.7.3.
- Normalization and formatting requirements are specified.
- `SKILL.md` support is specified in Section 2.7.4.
- Parse-failure behavior is defined in Section 2.7.6.

**Determination:** PASS

---

### Evaluation 8: Original Feature Preservation and Expanded System Continuity

**Criterion definition:**  
The redesigned app must preserve original features while adding new ones such as notifications and accounts.

**Evaluation logic/conditions:**
1. Confirm preservation intent is explicit.
2. Confirm original feature families remain represented.
3. Confirm notification system is specified.
4. Confirm account management system is specified.
5. Confirm expanded WOW features do not displace baseline features.

**Stepwise determination:**
- Preservation is stated in Executive Summary and throughout module descriptions.
- Dashboard, notes, skill/agent, workflow, settings, logs, and results center are all represented.
- Notifications are fully specified in Section 2.9.
- User account management is fully specified in Section 2.8.
- WOW additions are additive, not substitutive.

**Determination:** PASS

---

### Evaluation 9: Extensibility and Future-Proofing

**Criterion definition:**  
The app must be designed to absorb future models, languages, themes, and file schemas without structural rewrite.

**Evaluation logic/conditions:**
1. Confirm extensible model registry.
2. Confirm translation extensibility.
3. Confirm palette/theme extensibility.
4. Confirm file format growth path.
5. Confirm feature registration logic.

**Stepwise determination:**
- Extensible registry is defined in Section 2.10.1.
- Language expansion is covered in Sections 2.10.2 and 2.10.3.
- Theme expansion is covered in Section 2.10.4.
- File format growth is covered in Section 2.10.6.
- Feature registration metadata is defined in Section 2.10.5.

**Determination:** PASS

---

### Evaluation 10: Output Structure Compliance

**Criterion definition:**  
The response must follow the mandated structure and include required tables, evaluation logic, follow-up questions, and references.

**Evaluation logic/conditions:**
1. Check executive summary presence.
2. Check functional specification subsections presence.
3. Check both required tables.
4. Check ten quality evaluations with logic and determination.
5. Check twenty follow-up questions.
6. Check appendix/references.

**Stepwise determination:**
- Executive Summary is present as Section 1.
- Functional Specification is present as Section 2 with requested subsections.
- Design Decisions and WOW AI Features tables are present in Section 3.
- Ten evaluations are present in Section 4 with stepwise determination.
- Twenty follow-up questions are present in Section 5.
- Appendix/References are present in Section 6.

**Determination:** PASS

---

## 4.2 Quality Evaluation Summary Table

| Criterion | Result | Details |
|---|---|---|
| Requirement Coverage Completeness | PASS | All major requested functional, structural, and output requirements are covered |
| Deployment Feasibility for Local DGX-1 Hybrid Use | PASS | Local DGX-1/Ollama plus Gemini/OpenAI hybrid operation is explicitly supported |
| Security and Secret Handling Adequacy | PASS | Environment-secret concealment and secure handling expectations are defined |
| UX Personalization Completeness | PASS | Themes, zh-TW/en/ja, 10 palettes, and Jackpot are all specified |
| Observability and Live Visualization Adequacy | PASS | Animated execution, logs, dashboard, token telemetry, and degraded-mode handling are defined |
| AI Note Keeper Completeness | PASS | Input types, markdown transformation, coral keyword handling, edit modes, and 6 AI Magics are covered |
| Agent/Skill Module Precision | PASS | `agents.yaml` and `SKILL.md` actions, validation, standardization, and errors are fully specified |
| Original Feature Preservation and Expanded System Continuity | PASS | Original modules plus notifications and user accounts are preserved and extended |
| Extensibility and Future-Proofing | PASS | Registry, i18n, themes, features, and file-format growth paths are defined |
| Output Structure Compliance | PASS | Required section order, tables, evaluations, questions, and references are satisfied |

---

# 5. Follow-up Questions

1. For the local DGX-1 deployment, should the app prefer **native Ollama APIs** first, or should it treat an **OpenAI-compatible gateway** as the primary local protocol when both are available?

2. What is the expected authentication model for the local LLM host: **no auth on internal LAN**, **shared bearer token**, **per-user token**, or **mutual TLS / reverse proxy control**?

3. Should user accounts be strictly **local-app accounts**, or must the design reserve an upgrade path for **LDAP, OAuth, SSO, or enterprise identity integration**?

4. For secure user data persistence, is the preferred storage target a **local encrypted SQLite-equivalent**, a **file-backed secure store**, or a **remote internal database**?

5. Should guest mode be available by default, or should administrators be able to force **login-required mode** before any model invocation or file upload?

6. How should notification delivery behave for long-running tasks when the user navigates away from the browser tab: should the app support **browser notifications**, **in-app only**, or **email/webhook extensions** in future versions?

7. When a user enters API keys manually, should those keys persist only for the current session, or should there be an opt-in **encrypted local vault** for convenience?

8. For model selection, should the local host discovery process poll available models **on demand only**, **at startup**, or **on a periodic refresh schedule**?

9. Should the app allow simultaneous side-by-side evaluation across **one local model and one cloud model**, including shared input reuse and comparative token/runtime reporting?

10. For AI Note Keeper PDF ingestion, what quality threshold should trigger a “poor extraction” warning: **empty text only**, **page coverage threshold**, **OCR confidence threshold**, or a composite score?

11. Should coral-highlighted keywords remain a purely visual layer, or should exported markdown optionally embed a **portable inline annotation convention** for downstream systems?

12. For `agents.yaml` standardization, should the app enforce a strict internal schema, or should it support a **schema profile selector** for different agent ecosystems and versions?

13. For `SKILL.md`, do you want optional parsing of **YAML frontmatter metadata fields** such as title, provider hints, tags, version, and examples, or should markdown remain mostly freeform?

14. Should the WOW visualization support **run replay** so users can review a finished execution timeline as if it were streamed live?

15. In the notification preference system, do you want separate controls for **critical errors**, **task completions**, **feature news**, and **experimental feature notices**, or should categories remain broader for simplicity?

16. Should the Results/Downloads Center include **artifact lineage** that links an output note or skill file back to the exact provider, model, run ID, and source files used to generate it?

17. For local-only deployments in sensitive environments, should the system expose a **cloud egress kill switch** that hides Gemini/OpenAI selection entirely unless enabled by admin policy?

18. How much of the original eSub enterprise workflow should be activated in the single-file local edition: just the currently surfaced modules, or also a staged roadmap for **template studio**, **fill agent**, **pipeline execution**, and **regulatory evidence traceability**?

19. Should the app maintain a **compatibility mode** for future Anthropic integration from the start, even if the provider is not initially enabled in the UI?

20. What operational diagnostics are most important for your real environment: **connectivity tests**, **GPU/server availability checks**, **model list caching diagnostics**, **session state integrity checks**, or **startup self-test dashboards**?

---

# 6. Appendix/References

## 6.1 Terminology

- **DGX-1:** NVIDIA GPU server platform used here as the host for local inference services.
- **Ollama:** Local model serving system commonly used for self-hosted LLM access.
- **OpenAI-compatible endpoint:** Any local or remote endpoint exposing OpenAI-like request/response semantics.
- **Provider:** The service origin for inference, such as Gemini, OpenAI, Ollama, or a private gateway.
- **Model registry:** Structured inventory of known model IDs and capabilities.
- **WOW Sidebar:** Persistent contextual rail containing logs, token usage, shortcuts, and AI launchers.
- **AI Magics:** Note-centered AI enhancement tools.
- **WOW AI Features:** Platform-level AI assistance and observability functions.

## 6.2 YAML Reference Notes

Relevant behaviors for `agents.yaml` handling should align with stable YAML parsing and normalization expectations:
- UTF-8-safe handling
- Indentation normalization
- Top-level mapping validation
- Duplicate-key warning or error behavior depending on parser capability
- Safe-load semantics only

## 6.3 Markdown Reference Notes

Markdown handling should preserve:
- Headings
- Bullets and numbering
- Blockquotes
- Code fences if present in source notes
- Plain-text fallback compatibility

Color highlighting such as coral should be treated as a rendering annotation layer unless export mode explicitly supports a chosen inline convention.

## 6.4 Internationalization Notes

Recommended locale identifiers:
- `zh-TW`
- `en`
- `ja`

Translation keys should be stable, namespaced, and module-scoped.

## 6.5 Theme/Palette Notes

Pantone-inspired style systems should be translated into semantic design tokens such as:
- primary
- secondary
- accent
- success
- warning
- error
- info
- background
- surface
- border
- text-primary
- text-secondary

## 6.6 Provider/API Reference Notes

The provider abstraction should distinguish:
- Authentication requirements
- Streaming support
- Usage metrics support
- Structured output support
- Model discovery support
- Timeout behavior
- Error envelope structure

## 6.7 Reliability Notes

Blank-screen prevention in single-file Streamlit apps typically depends on:
- deterministic default state initialization
- defensive rendering fallbacks
- isolated state domains
- error surfaces visible in UI
- avoiding hidden dependency assumptions
- graceful degradation when provider/storage connectivity fails

## 6.8 Compliance With Requested Result Display Rule

All ten quality evaluations were assessed first. Because all ten passed, the evaluation summary table was displayed. If any criterion had failed, the summary table would have been withheld.