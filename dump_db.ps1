$timestamp = $(Get-Date).ToString('yyyyMMdd_HHmmss')

$Env:PGPASSWORD = 'password'; pg_dump -U postgres -d shuffle -F t -f ".\shuffle_latest.tar"
Write-Host "Local Database backed up to shuffle_latest.tar"