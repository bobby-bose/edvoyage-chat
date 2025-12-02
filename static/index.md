Overall visual summary
Platform: iOS-style mobile messaging list (single-column stack).
Visual feel: calm, soft, minimal, slightly warm/neutral background with a saturated teal/green primary for top navigation and call-to-action accents. High emphasis on readable typography and a clean list rhythm with very thin separators.
Key elements: top nav (back chevron + title), message list rows (avatar, name, preview, timestamp), thin horizontal separators, empty-state/label centered low-contrast (“De voyage”).
Color system (recommended design tokens)
Primary (navigation / brand): --color-primary: #118C6F (teal-green)
Primary dark: --color-primary-700: #0E775B
Primary light: --color-primary-100: #E7F5EE
Background (screen): --color-bg: #F3F4F4 (very light gray)
Surface / row: --color-surface: #FFFFFF (white)
Divider: --color-divider: #E1E1E1
Text (primary): --color-text: #212121 (near-black for names)
Text (secondary / preview): --color-muted: #727272
Timestamp / meta: --color-meta: #8E8E8E
Accent (error / heart): --color-accent-danger: #E53935
Empty state text: --color-empty: #D0D0D0
Rationale: primary ~#118C6F matches the teal in the masthead; background slightly warm gray for low-contrast canvas; dividers slightly darker than background to read as separators. Use semantic tokens so theme toggling (dark mode) is simple.

Typography & scale (iOS/typographic rhythm)
Font family: System UI / SF Pro (iOS). Fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial.
Title (nav): 22–24 sp, weight 600 (semibold). Color: primary.
List name: 17–18 sp, weight 600 (medium/semibold). Color: text.
Message preview: 13–14 sp, weight 400. Color: muted.
Timestamp: 12 sp, weight 500 or 400, color: meta.
Empty-state small label: 14 sp, weight 500, color: empty.
Line heights and vertical rhythm:

name line-height: ~22
preview line-height: ~18
Layout and spacing (component specs)
Screen safe insets: respect top/bottom safe area for notch and home indicator.
Screen padding: horizontal padding 16 px.
Row (message item) height: min 72–80 px (touch target >= 44 px, but for messaging rows, 72 typical).
Avatar:
Diameter: 56 px (circular)
Left margin from screen: 16 px
Content margin between avatar and text: 12–14 px
Name/timestamp row:
Name aligned left of text column; timestamp aligned to right edge of row (same baseline as name)
Timestamp right padding: 16 px
Preview text: below the name with 6–8 px vertical gap
Divider line:
Height: 1 px
Color: --color-divider
Left offset: aligned with the left edge of message text (i.e., left of divider = avatar left + avatar width + 12 px), so the divider visually separates rows without cutting through avatars
Empty state:
Center horizontally, vertical center located below the last row; typography muted and dashed decorative lines in same hue as empty state.
Component breakdown & API (MessageListItem)
Props: id, name, preview, timestamp, avatarUrl, unreadCount, onPress, onLongPress, isMuted, isOnline
Visual rules:
If unreadCount > 0: make name weight 700 and preview weight 600 and add small circular badge (background primary, text white) right aligned near timestamp
onPress: navigate to conversation with touch feedback (iOS highlight/opacity)
onLongPress: show context menu (archive, mute, delete)
Behavior: truncated preview to single line with trailing ellipsis
Interaction & animations
Row press animation: iOS-style opacity to 0.6 or scale 0.995 for 120ms, then back.
Navigation transition: native push with title fade/slide
Avatar image loading: crossfade 160ms; fall back to initials placeholder circle with neutral background if no image.
Separator appear/disappear: subtle fade with 100–150ms.
Accessibility & usability
Contrast:
Name vs background: >= 7:1 recommended — use near-black for name
Preview vs background: >= 4.5:1 — the chosen muted gray should meet this; test with WCAG tools
Touch targets: ensure each row’s tappable area >= 44x44 pt (we target 72 high to be safe)
VoiceOver / TalkBack:
Row accessibilityLabel: "{name}, {preview}, {timestamp}, {unread_count} unread"
Mark avatar as decorative unless it has meaningful alt text
Dynamic type: support accessibility font scaling; allow row height to grow or use truncation strategy and ensure layout remains usable
RTL: mirror layouts (timestamp left, name right), avatars remain on leading edge per locale
Performance & implementation suggestions
Use a virtualized list component (FlatList / RecyclerView) with keyExtractor = id
Use getItemLayout when rows uniform to improve scroll performance
Cache avatar images and use low-res placeholders
Avoid expensive shadow layers for each row (use simple 1px separators and background layering)
Lazy rendering of off-screen rows
Dark mode adaptation Example token swaps:
--color-bg: #0B0B0B
--color-surface: #111111
--color-text: #F5F5F5
--color-muted: #BDBDBD
--color-divider: rgba(255,255,255,0.06) Keep primary color similar but slightly brighter in dark mode (increase luminance).
Example style tokens & sample snippets
Design tokens (JSON-like): { "color": { "primary": "#118C6F", "bg": "#F3F4F4", "surface": "#FFFFFF", "divider": "#E1E1E1", "text": "#212121", "muted": "#727272", "meta": "#8E8E8E", "empty": "#D0D0D0", "danger": "#E53935" }, "spacing": { "screenPadding": 16, "avatar": 56, "gapItem": 12, "rowHeight": 76 }, "type": { "navTitle": 22, "name": 17, "preview": 14, "meta": 12 } }

React Native style example (abbreviated) /* JS/TS StyleSheet / container: { flex: 1, backgroundColor: tokens.color.bg, paddingTop: safeAreaTop }, nav: { height: 56, alignItems: 'center', flexDirection: 'row', paddingHorizontal: tokens.spacing.screenPadding, backgroundColor: tokens.color.surface }, navTitle: { fontSize: tokens.type.navTitle, color: tokens.color.primary, fontWeight: '600', marginLeft: 8 }, row: { minHeight: tokens.spacing.rowHeight, flexDirection: 'row', alignItems: 'center', paddingHorizontal: tokens.spacing.screenPadding, backgroundColor: tokens.color.surface }, avatar: { width: tokens.spacing.avatar, height: tokens.spacing.avatar, borderRadius: tokens.spacing.avatar / 2 }, textColumn: { flex: 1, marginLeft: tokens.spacing.gapItem, paddingRight: 64 / space for timestamp */ }, name: { fontSize: tokens.type.name, color: tokens.color.text, fontWeight: '600' }, preview: { fontSize: tokens.type.preview, color: tokens.color.muted, marginTop: 6 }, timestamp: { position: 'absolute', right: tokens.spacing.screenPadding, top: 18, fontSize: tokens.type.meta, color: tokens.color.meta }

Edge cases and polish
Handle empty list: show centered stub (“— De voyage —”) with dashed rules and subtle entrance animation.
Handle very long names: truncation with middle ellipsis for uniqueness if necessary.
Network errors for avatars: show initials; offer tap-to-retry for failed load if relevant.
Unread state: consider subtle background tint (primary-100) for a row to indicate unread — but test with contrast and visual noise.