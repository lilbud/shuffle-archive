$timestamp = $(Get-Date).ToString('yyyyMMdd_HHmmss')
$local_backup_dir = "C:\Users\bvw20\Documents\Personal\Projects\Bruce Stuff\Websites\e-street-shuffle\shuffle-archive"

$Env:PGPASSWORD='password'; pg_dump -U postgres -d shuffle -F t -f "$($local_backup_dir)\shuffle_$($timestamp).tar"
Write-Host "Local Database backed up to $($local_backup_dir)\shuffle_$($timestamp).tar"