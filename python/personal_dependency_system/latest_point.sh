#!/usr/bin/expect -f
set user         "inbox"
set password     "111qqq,,,\r"
set host         "10.10.24.13"

set remote_repo  "com.mapbar.qinjian.tools"
set _cd "cd"
set rm "rm"
set latest_version "ls | sort -n | tail -n 1"
set ln "ln -s"
set latest "latest"

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
proc create_soft_link {repo user host password} {
    global _cd
    global ln
    global latest_version
    #ln -s `ls |sort -n |tail -n 1` latest
    spawn ssh $user@$host $_cd $repo ";" $ln `$latest_version` latest
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
           latest
           latest_version
           ln
           password
           remote_repo
           rm
           user
       } {
    set latest_path [concat_repo_full_path $remote_repo $latest]
    set r [remove_file $latest_path $user $host $password]
    set r [create_soft_link $remote_repo $user $host $password ]
    exit $r
}

set _cd      [lindex $argv 0]
set host     [lindex $argv 1]
set latest   [lindex $argv 2]
set ln       [lindex $argv 3]
set password [lindex $argv 4]
set password [append password "\r"]
set repo     [lindex $argv 5]
set rm       [lindex $argv 6]
set user     [lindex $argv 7]
set version  [lindex $argv 8]

main $_cd $host $latest $version $ln $password $remote_repo $rm $user


