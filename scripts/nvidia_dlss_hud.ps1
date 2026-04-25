param(
    [ValidateSet('status', 'on', 'off')]
    [string]$State = 'status'
)

$keyPath = 'HKLM:\SOFTWARE\NVIDIA Corporation\Global\NGXCore'
$valueName = 'ShowDlssIndicator'
$enabledValue = 1024
$disabledValue = 0

function Get-HudStatus {
    $item = Get-ItemProperty -LiteralPath $keyPath -ErrorAction SilentlyContinue
    if ($null -eq $item -or $null -eq $item.$valueName) {
        [pscustomobject]@{
            Enabled = $false
            Value = $null
            Path = "$keyPath\$valueName"
            Message = 'DLSS HUD registry value is missing.'
        }
        return
    }

    $value = [int]$item.$valueName
    [pscustomobject]@{
        Enabled = $value -ne 0
        Value = $value
        Path = "$keyPath\$valueName"
        Message = if ($value -ne 0) { 'DLSS HUD is enabled.' } else { 'DLSS HUD is disabled.' }
    }
}

if ($State -eq 'status') {
    Get-HudStatus | Format-List
    exit 0
}

New-Item -Path $keyPath -Force | Out-Null
Set-ItemProperty -LiteralPath $keyPath -Name $valueName -Type DWord -Value $(if ($State -eq 'on') { $enabledValue } else { $disabledValue })
Get-HudStatus | Format-List
