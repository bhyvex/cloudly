###### Generate quick server load for testing

<pre>
$ openssl speed
</pre>

or ..

<pre>
root@monkey:~# while true
> do
> openssl speed
> sleep 60
> done
Doing md4 for 3s on 16 size blocks: ^C
root@monkey:~# ^C
root@monkey:~# ^C
root@monkey:~# while true; do openssl speed; sleep 180; done
Doing md4 for 3s on 16 size blocks: 12564847 md4's in 2.76s
Doing md4 for 3s on 64 size blocks: 9634040 md4's in 2.78s
Doing md4 for 3s on 256 size blocks: 5281405 md4's in 2.65s
Doing md4 for 3s on 1024 size blocks: 2043809 md4's in 2.76s
Doing md4 for 3s on 8192 size blocks: 299138 md4's in 2.76s
Doing md5 for 3s on 16 size blocks: 8452438 md5's in 2.72s
Doing md5 for 3s on 64 size blocks: 6087081 md5's in 2.67s
Doing md5 for 3s on 256 size blocks: 3486883 md5's in 2.78s
..
</pre>

