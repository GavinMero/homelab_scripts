$users = Import-Csv .\new_users.Csv

foreach ($user in $users) {


    $username = ($user.FirstName.Substring(0,1) + $user.LastName).ToLower()

    switch ($user.Department) {
        "IT" {
            $ou = "OU=IT,DC=ad,DC=merolab,DC=test"
        }
        "Finance" {
            $ou = "OU=Finance,DC=ad,DC=merolab,DC=test"
        }
        "Operations" {
            $ou = "OU=Operations,DC=ad,DC=merolab,DC=test"
        }
        default {
            Write-Host "Unknown department for $($user.FirstName) $($user.LastName)"
            continue
        }
    }

    $password = ConvertTo-SecureString "TempPass123!" -AsPlainText -Force

    New-ADUser `
        -Name "$($user.FirstName) $($user.LastName)" `
        -GivenName $user.FirstName `
        -Surname $user.LastName `
        -SamAccountName $username `
        -UserPrincipalName "$username@ad.merolab.test" `
        -Path $ou `
        -AccountPassword $password `
        -Enabled $true `
        -ChangePasswordAtLogon $true
    
    Write-Host "Created $username in $($user.Department)"

}