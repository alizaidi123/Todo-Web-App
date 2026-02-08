# API Base URL Contract

**Module**: `frontend/lib/apiBase.ts`
**Version**: 1.0.0
**Date**: 2026-02-08

## Public API

### `getApiBase(): string`

Returns the base URL for all backend API calls.

**Signature**:
```typescript
export function getApiBase(): string
```

**Returns**:
- `string` - Base URL without trailing slash (e.g., `https://api.example.com`)

**Throws**:
- `Error` - In production mode if no environment variables are configured

**Environment Variables** (priority order):
1. `NEXT_PUBLIC_API_BASE_URL` - Primary environment variable
2. `NEXT_PUBLIC_API_URL` - Secondary environment variable (fallback)

## Behavior Specification

### Production Mode

**Condition**: `process.env.NODE_ENV === 'production'`

| Env Vars | Behavior | Example |
|----------|----------|---------|
| `NEXT_PUBLIC_API_BASE_URL` set | Return value (normalized) | `https://api.example.com` |
| Only `NEXT_PUBLIC_API_URL` set | Return value (normalized) | `https://api.example.com` |
| Both set | Return `NEXT_PUBLIC_API_BASE_URL` | `https://api.example.com` |
| Neither set | **Throw Error** | `Error: API base URL not configured...` |

**Error Message**:
```
Error: API base URL not configured for production.
Please set NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL environment variable.
Current NODE_ENV: production
```

### Development Mode

**Condition**: `process.env.NODE_ENV === 'development'` or `NODE_ENV` is undefined

| Env Vars | Behavior | Console Warning |
|----------|----------|-----------------|
| `NEXT_PUBLIC_API_BASE_URL` set | Return value (normalized) | None |
| Only `NEXT_PUBLIC_API_URL` set | Return value (normalized) | None |
| Neither set | Return `http://127.0.0.1:8000` | Yes (warn about default) |

**Warning Message** (when using default):
```
Warning: API base URL not configured, using development default: http://127.0.0.1:8000
Set NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL to override.
```

### Normalization Rules

All returned values are normalized as follows:

1. **Trailing Slash Removal**: If URL ends with `/`, it is removed
   - Input: `https://api.example.com/`
   - Output: `https://api.example.com`

2. **No Leading/Trailing Whitespace**: Values are trimmed
   - Input: `  https://api.example.com  `
   - Output: `https://api.example.com`

## Usage Examples

### Production Usage (Vercel)

**Environment Variables**:
```bash
NEXT_PUBLIC_API_BASE_URL=https://alisaboor3-todo-app.hf.space
```

**Code**:
```typescript
import { getApiBase } from '@/lib/apiBase';

const API_BASE = getApiBase();
// Result: "https://alisaboor3-todo-app.hf.space"

fetch(`${API_BASE}/auth/login`, { ... });
// URL: "https://alisaboor3-todo-app.hf.space/auth/login"
```

### Development Usage (Local)

**No Environment Variables Set**

**Code**:
```typescript
import { getApiBase } from '@/lib/apiBase';

const API_BASE = getApiBase();
// Result: "http://127.0.0.1:8000"
// Console: Warning about using default

fetch(`${API_BASE}/auth/login`, { ... });
// URL: "http://127.0.0.1:8000/auth/login"
```

### Development with Custom Backend

**Environment Variables** (`.env.local`):
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
```

**Code**:
```typescript
import { getApiBase } from '@/lib/apiBase';

const API_BASE = getApiBase();
// Result: "http://localhost:5000"
// Console: No warning

fetch(`${API_BASE}/auth/login`, { ... });
// URL: "http://localhost:5000/auth/login"
```

## Migration from Legacy Code

**Old Pattern** (broken - module doesn't exist):
```typescript
import { getApiBaseUrl } from '@/lib/apiBase';

const API_BASE = getApiBaseUrl();
const url = `${API_BASE}/auth/login`;
```

**New Pattern**:
```typescript
import { getApiBase } from '@/lib/apiBase';

const API_BASE = getApiBase();
const url = `${API_BASE}/auth/login`;
```

**Changes**:
- Function renamed: `getApiBaseUrl()` → `getApiBase()`
- Behavior same in development
- **Breaking**: Production now throws if env vars missing (intentional)

## Testing

### Unit Test Cases

1. **Production with env var set**: Returns normalized URL
2. **Production without env vars**: Throws error with helpful message
3. **Development without env vars**: Returns localhost default + warning
4. **Development with env var set**: Returns configured URL
5. **Trailing slash normalization**: Removes trailing slash
6. **Whitespace handling**: Trims leading/trailing spaces
7. **Priority**: NEXT_PUBLIC_API_BASE_URL takes precedence over NEXT_PUBLIC_API_URL

### Integration Test Cases

1. **Build succeeds**: Production build with env vars set
2. **Build fails**: Production build without env vars
3. **API calls work**: Requests reach correct backend
4. **Local dev works**: Default localhost works without configuration

## Security Considerations

- ✅ No secrets in code (URLs from env vars)
- ✅ Fail fast prevents silent production errors
- ✅ Development default is safe (localhost only)
- ⚠️ Console warnings may expose backend URL (acceptable in dev mode)

## Performance

- **Build Time**: No impact (inlined during build)
- **Runtime**: Negligible (simple string operation, called once per module)
- **Bundle Size**: <100 bytes

## Versioning

**Version 1.0.0** (2026-02-08)
- Initial implementation
- Supports production and development modes
- Environment variable priority: NEXT_PUBLIC_API_BASE_URL > NEXT_PUBLIC_API_URL

**Future Considerations**:
- May add support for multiple backends (e.g., separate auth/data APIs)
- May add runtime override for testing purposes
- May add build-time validation script
