#!/usr/bin/expect -f
set user         "inbox"
set password     "111qqq,,,\r"
set host         "10.10.24.13"

set remote_repo  "com.mapbar.qinjian.tools"
set _cd "cd"
set rm "rm"
set ln "ln -s"
set stable "stable"
set stable_version "1.0.3"

proc remove_file {file_path user host password} {
    global rm
    spawn ssh $user@$host $rm $file_path
    expect "password: ";
    send $password;
    expect {
        eof {return 0}
        "No such file or directory" {return 1}
    };
}
proc create_stable_link {repo stable_version user host password} {
    global _cd
    global ln
    #ln -s `ls |sort -n |tail -n 1` latest
    spawn ssh $user@$host $_cd $repo ";" $ln $stable_version stable
    expect "password: ";
    send $password;
    expect {
        eof {return 0}
        "No such file or directory" {return 1}
    };
}

proc concat_repo_full_path {repo version} {
    set prefix [append repo "/"]
    set full_path [append prefix $version]
    return $full_path
}

proc main {
           _cd
           host
           ln
           password
           remote_repo
           rm
           stable
           stable_version
           user
       } {
    set stable_path [concat_repo_full_path $remote_repo $stable]
    set r [remove_file $stable_path $user $host $password]
    set r [create_stable_link $remote_repo $stable_version $user $host $password ]
    exit $r
}

set _cd      [lindex $argv 0]
set host     [lindex $argv 1]
set ln       [lindex $argv 2]
set password [lindex $argv 3]
set password [append password "\r"]
set repo     [lindex $argv 4]
set rm       [lindex $argv 5]
set stable   [lindex $argv 6]
set user     [lindex $argv 7]
set version  [lindex $argv 8]

main $_cd $host $ln $password $repo $rm $stable $version $user
