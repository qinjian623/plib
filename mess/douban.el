(require 'emms)
(require 'json)

(defface douban-music-title-face
  '((t (:height 2.05 :foreground "Grey65")))
  "Face for douban music title"
  :group 'qjdb)

(defconst douban-music-buffer-name "*Douban.FM*")

(defconst douban-music-channels-url "http://www.douban.com/j/app/radio/channels")

(defvar douban-music-channels nil)


(defun qjdb-split-http-header (s)
  (second (split-string s "\n\n")))

(defun qjdb-insert-cover-async (picture-url)
  (url-retrieve
   picture-url
   (lambda (s)
     (let ((img (create-image (qjdb-split-http-header (buffer-string)) nil 'f)))
       (with-current-buffer (get-buffer-create  douban-music-buffer-name)
         (insert-image img))))))

(defun display-info (title album artist picture-url)
  (let ((oldbuf (current-buffer)))
    (with-current-buffer (get-buffer-create douban-music-buffer-name)
      (erase-buffer)
      (insert (propertize title 'face 'douban-music-title-face) "\n")
      (qjdb-insert-cover-async picture-url) nil 'f)))

(display-info "asdf" "asdf" "asdf" "http://img3.douban.com/lpic/s4712330.jpg")





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

(defun qjdb-parse-channels-json (json-string)

  (let (channels (cdr
                  (assoc 'channels
                         (json-read-from-string
                          (decode-coding-string json-string 'utf-8)))))
    (message channels)
    (dotimes (i (length channels))
      (let ((var (nth i channels )))
        (message i)
        (setq douban-music-channels
              (cons
               (cons (cdr (assoc 'channel_id var))
                     (cdr (assoc 'name var)))
               douban-music-channels))))
    ))

(defun qjdb-get-channels ()
  (qjdb-parse-channels-json
   (with-current-buffer (douban-music-send-url douban-music-channels-url)
     (qjdb-split-http-header (buffer-string)))))

(qjdb-get-channels)
( douban-music-channels)
(decode-coding-string )
(defun qjdb-insert-cover-sync (picture-url)
  (with-current-buffer (get-buffer-create douban-music-buffer-name))
  (insert-image (create-image
                 (with-current-buffer (douban-music-send-url picture-url)
                   (qjdb-split-http-header (buffer-string))) nil 'f)))

(defun qjdb-play-song (song-url)
  (emms-play-url song-url))

(defun qjdb-pause-or-play-song
  (emms-pause))
(defun qjdb-stop-song
  (emms-stop))


(defun qjdb-next-song)
(defun qjdb-jump-song)
(defun qjdb-like-song)
(defun qjdb-ban-song)









