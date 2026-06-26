# Task Analyzer - Cursor Enterprise Framework
# Version: 1.0.0

param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string]$Request = "",
    [switch]$Analyze,
    [switch]$ListSkills,
    [switch]$ListMCP,
    [switch]$CheckContext
)

# Helper functions
function _step($m) { Write-Host "[STEP] $m" -ForegroundColor Cyan }
function _ok($m) { Write-Host "[OK] $m" -ForegroundColor Green }
function _warn($m) { Write-Host "[WARN] $m" -ForegroundColor Yellow }
function _header($t) {
    Write-Host ""
    Write-Host ("=" * 80) -ForegroundColor Magenta
    Write-Host "[$t]" -ForegroundColor Magenta
    Write-Host ("=" * 80) -ForegroundColor Magenta
}

# Language Detection
function Get-Lang($text) {
    $t = $text.ToLower()
    # Check CJK first (most distinctive)
    if ($text -match "[\u4e00-\u9fff]") { return "chinese" }
    if ($text -match "[\u3040-\u309f\u30a0-\u30ff]") { return "japanese" }
    if ($text -match "[\uac00-\ud7af]") { return "korean" }
    # Vietnamese signals (ASCII-safe)
    $viWords = @("tao", "xay dung", "cai thien", "sua loi", "thiet ke", "trang", "cua", "la", "duoc", "voi", "va")
    $viScore = 0
    foreach ($w in $viWords) { if ($t.Contains($w)) { $viScore++ } }
    # English signals
    $enWords = @("create", "build", "improve", "fix", "design", "page", "landing", "with", "and", "for")
    $enScore = 0
    foreach ($w in $enWords) { if ($t.Contains($w)) { $enScore++ } }
    if ($viScore -gt $enScore) { return "vietnamese" }
    return "english"
}

# Intent Analysis
function Get-Intent($text) {
    $t = $text.ToLower()
    $scores = @{}
    $map = @{
        "build"=@("create","build","make","add","implement","tao","xay dung")
        "redesign"=@("improve","upgrade","redesign","modernize","enhance","cai thien")
        "fix"=@("fix","bug","error","issue","repair","debug","sua loi")
        "review"=@("review","check","audit","analyze","kiem tra")
        "security"=@("security","vulnerability","auth","JWT","bao mat","pentest")
    }
    foreach ($n in $map.Keys) {
        $scores[$n] = 0
        foreach ($k in $map[$n]) { if ($t -match $k) { $scores[$n]++ } }
    }
    $max = 0; $primary = "build"
    foreach ($n in $scores.Keys) { if ($scores[$n] -gt $max) { $max = $scores[$n]; $primary = $n } }
    
    $doms = @()
    $dmap = @{
        "frontend"=@("frontend","UI","landing","page","component","react","vue","next","tailwind","landing page","tao trang","trang dich","website","giao dien","web")
        "backend"=@("backend","API","server","endpoint","database","rest","graphql")
        "security"=@("security","auth","vulnerability","JWT","XSS","pentest","owasp")
        "payment"=@("payment","MoMo","SePay","PayOS","VNPay","ZaloPay","VietQR","thanhtoan","momo","thanh toan","payment gateway")
        "knowledge"=@("knowledge","RAG","wiki","FAQ","weknora","rag","tri thuc")
    }
    foreach ($d in $dmap.Keys) {
        foreach ($p in $dmap[$d]) { if ($t -match $p) { $doms += $d; break } }
    }
    
    return @{primary=$primary; domains=$doms; primary_domain=if($doms.Count -gt 0){$doms[0]}else{"general"}}
}

# Skill Detection
function Get-Skills($text, $intent) {
    $t = $text.ToLower()
    $matched = @()
    $conf = @{}
    
    # Skill definitions: id -> @(keywords, threshold, always_frontend, mandatory)
    # Using simple contains matching for reliability
    $defs = @{
        "frontend-taste"=@(@("landing page","portfolio","homepage","marketing","saas","greenfield","beautiful","trang dich","danh muc","tao landing","tao trang"),0.5,$true,$false)
        "frontend-redesign"=@(@("redesign","upgrade","improve existing","modernize","cai thien","hien tai","cai tien giao dien","website hien tai","website hien tai","cai thien giao dien"),0.5,$true,$false)
        "full-output"=@(@("full implementation","complete","not skeleton","no todo","entire","hoan chinh","toan bo","trien khai day du"),0.5,$false,$false)
        "frontend-review"=@(@("review","quality check","audit","taste check","kiem tra","danh gia","chat luong","quality"),0.4,$true,$true)
        "security-review"=@(@("security","vulnerability","xss","sql injection","auth","jwt","pentest","owasp","bao mat","lo hong"),0.5,$false,$false)
        "vietnam-payment-review"=@(@("momo","sepay","payos","vnpay","zalopay","vietqr","thanh toan","payment"),0.5,$false,$false)
        "karpathy-coding"=@(@("vibe code","simple","straightforward","minimal","dont overthink","don gian","don gian"),0.4,$false,$true)
        "ponytail"=@(@("less code","yagni","over-engineering","over engineering","it code"),0.5,$false,$false)
        "visual-explainer"=@(@("diagram","architecture","flowchart","diff review","so do"),0.5,$false,$false)
        "weknora-kb"=@(@("knowledge base","rag","wiki","faq","weknora","co so tri thuc","tri thuc"),0.5,$false,$false)
        "pixelrag"=@(@("pixelrag","visual rag","screenshot rag","table extraction","doc bang","doc bieu do"),0.5,$false,$false)
        "document-ocr"=@(@("ocr","text extraction","image to text","scanned","doc text","trich xuat"),0.5,$false,$false)
    }
    
    foreach ($sid in $defs.Keys) {
        $d = $defs[$sid]
        $kws = $d[0]; $thresh = $d[1]; $alwaysFE = $d[2]; $mandatory = $d[3]
        $score = 0
        $matched_kws = @()
        foreach ($k in $kws) { 
            # Use simple contains for single words, exact match for phrases
            if ($k.Contains(" ")) {
                if ($t.Contains($k)) { $score += 2; $matched_kws += $k }
            } else {
                if ($t -like "*$k*") { $score++; $matched_kws += $k }
            }
        }
        # Confidence based on matched keywords count, threshold is minimum matches
        $c = $matched_kws.Count
        
        if ($mandatory) {
            $matched += $sid
            $conf[$sid] = 1.0
        }
        elseif ($c -ge 1) {  # Match if at least 1 keyword found
            if ($alwaysFE -and ($intent.domains -contains "frontend")) {
                $matched += $sid
                $conf[$sid] = [Math]::Min($c * 0.3, 1.0)  # Cap at 1.0
            }
            elseif (-not $alwaysFE) {
                $matched += $sid
                $conf[$sid] = [Math]::Min($c * 0.3, 1.0)
            }
        }
    }
    
    $primary = $null
    $highest = 0
    foreach ($s in $matched) {
        if ($s -notin @("karpathy-coding","frontend-review") -and $conf[$s] -gt $highest) {
            $highest = $conf[$s]
            $primary = $s
        }
    }
    
    return @{matched=$matched; conf=$conf; primary=$primary; total=$matched.Count}
}

# Task Generation
function Get-Tasks($skills) {
    $tasks = @()
    $pre = @(); $post = @()
    
    $gm = @{
        "karpathy-coding"=@{p=@("karpathy-pre");q=@("karpathy-post")}
        "frontend-taste"=@{p=@("taste-pre");q=@("taste-post")}
        "frontend-redesign"=@{p=@("redesign-pre");q=@("redesign-post")}
        "full-output"=@{p=@("fulloutput-pre");q=@("fulloutput-post")}
        "frontend-review"=@{p=@("review-pre");q=@("review-post")}
        "security-review"=@{p=@("security-pre");q=@("security-post")}
        "vietnam-payment-review"=@{p=@("payment-pre");q=@("payment-post")}
        "weknora-kb"=@{p=@("weknora-pre");q=@("weknora-post")}
        "pixelrag"=@{p=@("pixelrag-pre");q=@("pixelrag-post")}
        "document-ocr"=@{p=@("ocr-pre");q=@("ocr-post")}
    }
    
    foreach ($s in $skills.matched) {
        if ($gm.ContainsKey($s)) {
            $pre += $gm[$s].p
            $post += $gm[$s].q
        }
    }
    $pre = $pre | Select-Object -Unique
    $post = $post | Select-Object -Unique
    
    $tid = 1
    if ($pre.Count -gt 0) {
        $sub = @()
        foreach ($g in $pre) { $sub += @{n="$g";c=@("Initialized","Reviewed","Passed")} }
        $tasks += @{id="task-$tid";n="Pre-Review Gates";t="pre-gate";d="Run all pre-review gates";s=$sub}
        $tid++
    }
    
    $implSub = @(
        @{n="Environment Setup";c=@("Dependencies installed","Configured")},
        @{n="Core Implementation";c=@("Logic implemented","Follows style")},
        @{n="Testing";c=@("Tests written","Tests pass")}
    )
    $dep = if($tasks.Count -gt 0){"task-$($tid-1)"}else{$null}
    $tasks += @{id="task-$tid";n="Implementation";t="implementation";d="Implement requested feature";s=$implSub;dep=$dep}
    $tid++
    
    if ($post.Count -gt 0) {
        $sub = @()
        foreach ($g in $post) { $sub += @{n="$g";c=@("Initialized","Reviewed","Passed")} }
        $tasks += @{id="task-$tid";n="Post-Review Gates";t="post-gate";d="Run all post-review gates";s=$sub;dep="task-$($tid-1)"}
        $tid++
    }
    
    $delSub = @(@{n="Final Review";c=@("Code reviewed")},@{n="Deliver";c=@("Code delivered")})
    $tasks += @{id="task-$tid";n="Delivery";t="delivery";d="Deliver final code";s=$delSub;dep="task-$($tid-1)"}
    
    return $tasks
}

# List Skills
function Show-Skills {
    _header "AVAILABLE SKILLS"
    $list = @(
        @{id="frontend-taste";d="Landing pages, portfolios, premium design [pre/post]"},
        @{id="frontend-redesign";d="Redesign existing UI [pre/post]"},
        @{id="full-output";d="Complete implementation [pre/post]"},
        @{id="frontend-review";d="Quality review [MANDATORY] [pre/post]"},
        @{id="security-review";d="Security vulnerability [pre/post]"},
        @{id="vietnam-payment-review";d="MoMo, SePay, PayOS, VNPay, ZaloPay, VietQR [pre/post]"},
        @{id="karpathy-coding";d="Vibe coding discipline [MANDATORY] [pre/post]"},
        @{id="ponytail";d="Minimal code, YAGNI"},
        @{id="visual-explainer";d="Diagrams, architecture overviews"},
        @{id="weknora-kb";d="Knowledge base, RAG, wiki [pre/post]"},
        @{id="pixelrag";d="Visual RAG [pre/post]"},
        @{id="document-ocr";d="Text extraction from images [pre/post]"}
    )
    foreach ($s in $list) {
        Write-Host ""
        Write-Host "  $($s.id)" -ForegroundColor Cyan
        Write-Host "    $($s.d)"
    }
    Write-Host ""
    _ok "Total: $($list.Count) skills"
}

# List MCP
function Show-MCP {
    _header "MCP SERVERS"
    $basePath = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
    
    # Try multiple potential locations
    $possiblePaths = @(
        (Join-Path $basePath ".cursor\mcps"),
        (Join-Path $basePath "mcps"),
        "$env:USERPROFILE\.cursor\mcps",
        "$env:APPDATA\Cursor\cursor-mcp"
    )
    
    $found = $false
    foreach ($mcpPath in $possiblePaths) {
        if (Test-Path $mcpPath) {
            $servers = Get-ChildItem -Path $mcpPath -Directory -ErrorAction SilentlyContinue
            if ($servers) {
                $found = $true
                foreach ($srv in $servers) {
                    $meta = Join-Path $srv.FullName "SERVER_METADATA.json"
                    if (Test-Path $meta) {
                        try {
                            $m = Get-Content $meta -Raw | ConvertFrom-Json
                            Write-Host ""
                            Write-Host "  $($m.serverName)" -ForegroundColor Cyan
                            Write-Host "    ID: $($m.serverIdentifier)"
                        } catch {}
                    }
                }
                Write-Host ""
                _ok "Total: $($servers.Count) servers at $mcpPath"
            }
        }
    }
    
    if (-not $found) {
        Write-Host ""
        Write-Host "  Note: MCP servers are configured in Cursor global settings" -ForegroundColor Gray
        Write-Host "  Check: Settings > MCP Servers" -ForegroundColor Gray
        _ok "MCP configured globally"
    }
}

# Check Context
function Show-Context {
    _header "CONTEXT REGISTRY"
    $basePath = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
    
    $rulesDir = Join-Path $basePath ".cursor\rules"
    $skillsDir = Join-Path $basePath ".cursor\skills"
    $mcpDir = Join-Path $basePath ".cursor\mcps"
    
    Write-Host ""
    Write-Host "Rules:" -ForegroundColor Yellow
    if (Test-Path $rulesDir) { $rc = (Get-ChildItem $rulesDir -Filter "*.mdc" -ErrorAction SilentlyContinue).Count; _ok "Total: $rc" }
    else { _warn "Not found" }
    
    Write-Host ""
    Write-Host "Skills:" -ForegroundColor Yellow
    if (Test-Path $skillsDir) { $sc = (Get-ChildItem $skillsDir -Directory -ErrorAction SilentlyContinue).Count; _ok "Total: $sc" }
    else { _warn "Not found" }
    
    Write-Host ""
    Write-Host "MCP Servers:" -ForegroundColor Yellow
    if (Test-Path $mcpDir) { $mc = (Get-ChildItem $mcpDir -Directory -ErrorAction SilentlyContinue).Count; _ok "Total: $mc" }
    else {
        Write-Host "  Note: MCP servers are configured in Cursor global settings" -ForegroundColor Gray
        _ok "Configured globally"
    }
    
    Write-Host ""
    Write-Host "Libraries:" -ForegroundColor Yellow
    _ok "Python: $(python --version 2>&1 | Select-Object -First 1)"
    _ok "Node: $(node --version 2>&1 | Select-Object -First 1)"
    _ok "PowerShell: $($PSVersionTable.PSVersion)"
    
    _ok "Context loaded"
}

# Analyze Request
function Invoke-Analyze($req) {
    _header "ANALYZING REQUEST"
    Write-Host ""
    Write-Host "Request: $req" -ForegroundColor White
    
    _step "Detecting language..."
    $lang = Get-Lang -text $req
    Write-Host "  Language: $lang"
    
    _step "Analyzing intent..."
    $intent = Get-Intent -text $req
    Write-Host "  Primary: $($intent.primary)"
    Write-Host "  Domains: $($intent.domains -join ', ')"
    
    _step "Detecting skills..."
    $skills = Get-Skills -text $req -intent $intent
    Write-Host "  Found $($skills.total) skills:"
    foreach ($s in $skills.matched) {
        $c = $skills.conf[$s]
        $role = if($s -eq $skills.primary){"PRIMARY"}elseif($s -eq "karpathy-coding"){"OVERLAY"}else{"secondary"}
        Write-Host "    - $s ($([Math]::Round($c*100))%) [$role]"
    }
    
    _step "Generating tasks..."
    $tasks = Get-Tasks -skills $skills
    Write-Host ""
    Write-Host "Task Manifest:" -ForegroundColor Yellow
    foreach ($t in $tasks) {
        $dep = if($t.dep){" [dep: $($t.dep)]"}else{""}
        Write-Host "  - $($t.id): $($t.n)$dep"
        foreach ($st in $t.s) { Write-Host "      -> $($st.n)" }
    }
    
    _ok "Analysis complete!"
}

# Main
if ($ListSkills) { Show-Skills; exit 0 }
if ($ListMCP) { Show-MCP; exit 0 }
if ($CheckContext) { Show-Context; exit 0 }

if ($Request -eq "") {
    Write-Host ""
    Write-Host "Task Analyzer - Cursor Enterprise Framework v1.0.0" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host '  .\.cursor\scripts\task-analyzer.ps1 -Request "your request"'
    Write-Host "  .\.cursor\scripts\task-analyzer.ps1 -ListSkills"
    Write-Host "  .\.cursor\scripts\task-analyzer.ps1 -ListMCP"
    Write-Host "  .\.cursor\scripts\task-analyzer.ps1 -CheckContext"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host '  .\.cursor\scripts\task-analyzer.ps1 -Request "Tao landing page dep"'
    Write-Host '  .\.cursor\scripts\task-analyzer.ps1 -Request "Fix login bug"'
    Write-Host '  .\.cursor\scripts\task-analyzer.ps1 -Request "Add MoMo payment"'
    Write-Host ""
    exit 0
}

Invoke-Analyze -req $Request
