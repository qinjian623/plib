#!/usr/bin/expect -f
proc concat_repo_full_path {repo version} {
    set prefix [append repo "/"];
    set full_path [append prefix $version];
    return $full_path;
}
proc add_star {path} {
    return [append path "*"]
}

proc sync_one_file {host one_file local_folder password remote_repo rsync version user} {
    set remote_repo_version [concat_repo_full_path $remote_repo $version]
    set jar_file_path $one_file
    #set jar_file_path       [concat_repo_full_path $local_folder $one_file]
    #set jar_file_path       [add_star $jar_file_path]
    spawn $rsync $jar_file_path $user@$host:$remote_repo_version
    expect "assword: ";
    send $password;
    expect {
        eof      {return 0}
        "exists" {return 1}
        "denied" {return 2}
    };
}
proc main {
    host
    jar_file
    local_folder
    password
    remote_repo
    rsync
    user
    version
} {
    foreach file_name [lsort [glob -dir $local_folder *]] {
        sync_one_file $host $file_name $local_folder $password $remote_repo $rsync $version $user
    }
}

set host         [lindex $argv 0]
set local_folder [lindex $argv 1]
set password     [lindex $argv 2]
set password     [append password "\r"]
set repo         [lindex $argv 3]
set rsync        [lindex $argv 4]
set user         [lindex $argv 5]
set version      [lindex $argv 6]

main $host "" $local_folder $password $repo $rsync $user $version

