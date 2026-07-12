$headers = @{'Accept'='application/vnd.github+json'}
for ($i = 0; $i -lt 18; $i++) {
  $r = (Invoke-WebRequest -Uri 'https://api.github.com/repos/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/pulls?state=open&head=minhkiet:chore/readme-clarity' -UseBasicParsing -Headers $headers).Content
  if ($r -ne '[]') {
    Write-Host 'PR_OPENED'
    Write-Host $r
    exit 0
  }
  Write-Host "poll $i no PR"
  Start-Sleep -Seconds 5
}
Write-Host 'PR_NOT_OPENED_TIMEOUT'
exit 1
