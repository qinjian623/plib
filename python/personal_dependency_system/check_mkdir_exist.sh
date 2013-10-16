#!/usr/bin/expect -f
set user         "inbox"
set password     "111qqq,,,\r"
set host         "10.10.24.13"

set version      "1.0.2"
set remote_repo  "com.mapbar.qinjian.tools"
set mkdir        "mkdir"


proc concat_repo_full_path {repo version} {
    set prefix [append repo "/"];
    set full_path [append prefix $version];
    return $full_path;
}

proc creat_remote_dir {remote_dir user host password} {
    global mkdir
    spawn ssh $user@$host $mkdir $remote_dir;
    expect "password: ";
    send $password;
    expect {
        eof {return 0}
        "exists" {return 1}
        "denied" {return 2}
    };
}

proc main {
           host
           mkdir
           password
           remote_repo
           user
           version
       } {
    set repo_exists [creat_remote_dir $remote_repo $user $host $password]
    if {$repo_exists != 0} {
        puts stderr "该软件库空间已经存在。";
    }

    set full_path [concat_repo_full_path $remote_repo $version]
    set version_exists [creat_remote_dir $full_path $user $host $password]
    if {$version_exists != 0} {
        puts stderr "该版本已经存在。";
        exit 1
    }
}

set host         [lindex $argv 0]
set mkdir        [lindex $argv 1]
set password     [lindex $argv 2]
set password     [append password "\r"]
set remote_repo  [lindex $argv 3]
set user         [lindex $argv 4]
set version      [lindex $argv 5]
main $host $mkdir $password $remote_repo $user $version


