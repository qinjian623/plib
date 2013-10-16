#!/usr/bin/expect -f
proc concat_repo_full_path {repo version} {
    set prefix [append repo "/"];
    set full_path [append prefix $version];
    return $full_path;
}

proc add_path_suffix {path} {
    return [append path "/"]
}
proc add_star {path} {
    return [append path "*"]
}

proc main {
           host
           local_folder
           password
           remote_repo
           rsync
           user
           version } {
    set remote_repo_version [concat_repo_full_path $remote_repo $version]
    set remote_repo_version [add_path_suffix $remote_repo_version]
    set remote_repo_version [add_star $remote_repo_version]
    set local_folder [add_path_suffix $local_folder]
    spawn $rsync $user@$host:$remote_repo_version $local_folder
    expect "assword: "
    send $password
    expect {
        eof {return 0}
        "exists" {return 1}
        "denied" {return 2}
    }
}


set host         [lindex $argv 0]
set local_folder [lindex $argv 1]
set password     [lindex $argv 2]
set password     [append password "\r"]
set remote_repo  [lindex $argv 3]
set rsync        [lindex $argv 4]
set user         [lindex $argv 5]
set version      [lindex $argv 6]
main $host $local_folder $password $remote_repo $rsync $user $version

