(require 'emms)
(require 'json)

(defface douban-music-title-face
  '((t (:height 2.05 :foreground "Grey65")))
  "Face for douban music title"
  :group 'qjdb)

(defconst douban-music-buffer-name "*Douban.FM*")
(defconst douban-music-max-songs-list 5)
(defconst douban-music-channels-url "http://www.douban.com/j/app/radio/channels")
(defconst douban-music-get-song-list-url "http://www.douban.com/j/app/radio/people?app_name=radio_desktop_win&version=100&channel=%s&type=n")
(defconst douban-music-default-channel 1)
(defconst douban-music-default-song 0)

(defvar douban-music-channels nil)
(defvar douban-music-current-channel 1)

(defvar douban-music-songs nil)
(defvar douban-music-current-song nil)

(defun qjdb-split-http-header (s)
  (second (split-string s "\n\n")))

(defun qjdb-insert-cover-async (picture-url)
  (url-retrieve
   picture-url
   (lambda (s)
     (let ((img (create-image (qjdb-split-http-header (buffer-string)) nil 'f)))
       (with-current-buffer (get-buffer-create  douban-music-buffer-name)
         (insert-image img))))))

(defun qjdb-display-info (title album artist picture-url)
  (let ((oldbuf (current-buffer)))
    (with-current-buffer (get-buffer-create douban-music-buffer-name)
      (erase-buffer)
      (insert (propertize title 'face 'douban-music-title-face) "\n")
      (qjdb-insert-cover-async picture-url) nil 'f)))

(defun qjdb-parse-list-json (json-string json-field func)
  (let ((items
         (cdr
          (assoc json-field
                 (json-read-from-string
                  (decode-coding-string json-string 'utf-8))))))
    (mapcar func items)))

(defun qjdb-parse-channels-json (json-string)
  (qjdb-parse-list-json json-string 'channels
                        (lambda (item)
                          (cons (cdr (assoc 'channel_id item))
                                (cdr (assoc 'name item))))))
(defun qjdb-get-channels-from-web ()
  (qjdb-parse-channels-json
   (with-current-buffer (douban-music-send-url douban-music-channels-url)
     (qjdb-split-http-header (buffer-string)))))

(defun qjdb-set-channels()
  (progn
    (setq douban-music-channels
          (qjdb-get-channels-from-web))
    (setq douban-music-current-channel 1)))

(defun qjdb-parse-songs-json (json-string)
  (qjdb-parse-list-json json-string 'song
                        (lambda (item)
                          (progn
                            item))))

(defun qjdb-get-songs-from-web (channel-number)
  (qjdb-parse-songs-json
   (with-current-buffer
       (douban-music-send-url (format douban-music-get-song-list-url channel-number))
     (qjdb-split-http-header (buffer-string)))))

(defun qjdb-set-songs (channel-number)
  (progn
    (setq douban-music-songs
          (qjdb-get-songs-from-web channel-number))
    (setq douban-music-current-song 0)))


(defun douban-music-send-url (url &optional url-args callback callback-args)
  "Fetch data from douban music server."
  (let ((url-request-method "GET"))
    (if url-args
        (setq url-request-data (mapconcat #'(lambda (arg)
                                              (concat (url-hexify-string (car arg))
                                                      "="
                                                      (url-hexify-string (cdr arg))))
                                          url-args "&")))
    (if callback
        (url-retrieve url callback callback-args)
      (url-retrieve-synchronously url))))

(defun qjdb-insert-cover-sync (picture-url)
  (with-current-buffer (get-buffer-create douban-music-buffer-name))
  (insert-image (create-image
                 (with-current-buffer (douban-music-send-url picture-url)
                   (qjdb-split-http-header (buffer-string))) nil 'f)))

(defun qjdb-play-song (song-url)
  (emms-play-url song-url))
(defun qjdb-pause-or-play-song ()
  (emms-pause))
(defun qjdb-stop-song ()
  (emms-stop))
(qjdb-pause-or-play-song)
(qjdb-stop-song)
(defun pick-nth-song-url (n)
  (cdr (assoc 'url (nth n douban-music-songs))))

(defun qjdb-set-current-channel (n)
  (if (not (assoc n douban-music-channels))
      (setq douban-music-current-channel n)))

(defun qjdb-next-song ()
  (let ((song-url (pick-nth-song-url (+ 1 douban-music-current-song))))
    (if (not song-url)
        (progn
          (message "REGET songs list from web")
          (message (format "%d" douban-music-current-song))
          (message (format "%d"  douban-music-current-channel))
          (qjdb-set-songs douban-music-current-channel)
          (qjdb-next-song))
      (progn
        (message (format "%d" douban-music-current-song))
        (message (format "%d" douban-music-current-channel))
        (qjdb-play-song song-url)
        (setq douban-music-current-song
              (+ 1 douban-music-current-song))))))

(defun qjdb-jump-song ()
  (progn
    (qjdb-set-songs douban-music-current-channel)
    (qjdb-next-song)))

(qjdb-set-songs 1)
(setq douban-music-current-song 1)
(douban-music-songs)
(qjdb-set-channels)
(qjdb-next-song)
(qjdb-jump-song)

;;TODO
(defun qjdb-like-song ())
(defun qjdb-ban-song ())

