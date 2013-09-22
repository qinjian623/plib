(require 'emms)
(require 'json)

(defface douban-music-title-face
  '((t (:height 2.05 :foreground "Grey65")))
  "Face for douban music title"
  :group 'qjdb)

(defconst douban-music-buffer-name "*Douban.FM*")
(defconst douban-music-max-songs-list 5)
(defconst douban-music-channels-url
  "http://www.douban.com/j/app/radio/channels")

;; From http://blog.yanunon.com/2012/07/download-douban-fm-liked.html
(defconst douban-music-get-song-list-url "http://www.douban.com/j/app/radio/people?app_name=radio_desktop_win&version=100&channel=%s&type=n")
(defconst douban-music-login-url "http://www.douban.com/j/app/login")

(defconst douban-music-default-channel 1)
(defconst douban-music-default-song 0)

(defvar douban-music-email nil)
(defvar douban-music-user-name nil)
(defvar douban-music-expire nil)
(defvar douban-music-user-id nil)
(defvar douban-music-token nil)
(defvar douban-music-r 1)

(defvar douban-music-channels nil)
(defvar douban-music-current-channel 1)

(defvar douban-music-songs nil)
(defvar douban-music-current-song 0)

(defvar qjdb-mode-line-string "")

(defun qjdb-split-http-header (s)
  (second (split-string s "\n\n")))

(defun qjdb-insert-cover-async (picture-url)
  (url-retrieve
   picture-url
   (lambda (s)
     (let((img
           (create-image
            (qjdb-split-http-header (buffer-string)) nil 'f)))
       (with-current-buffer
           (get-buffer-create  douban-music-buffer-name)
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


(defun qjdb-parse-login-info-json (json-string)
  (let ((json (json-read-from-string
                 (decode-coding-string json-string 'utf-8))))
    (if (/= (cdr (assoc 'r json)) 0)
        (message "LOGIN PARSE ERROR")
      (progn
        (setq douban-music-r (cdr (assoc 'r json)))
        (setq douban-music-token (cdr (assoc 'token json)))
        (setq douban-music-email (cdr (assoc 'email json)))
        (setq douban-music-user-name (cdr (assoc 'user_name json)))
        (setq douban-music-expire (cdr (assoc 'expire json)))
        (setq douban-music-user-id (cdr (assoc 'user_id json)))))))

(defun my-url-http-post (url args)
  (let ((url-request-method "POST")
        (url-request-extra-headers
             '(("Content-Type" . "application/x-www-form-urlencoded")))
        (url-request-data
         (mapconcat (lambda (arg)
                      (concat (car arg)
                              "="
                              (cdr arg)
                              ))
                    args
                    "&")))
    (url-retrieve-synchronously url)))

(qjdb-parse-login-info-json
 (with-current-buffer
     (my-url-http-post douban-music-login-url
                       (list
                        '("username" . "qinjian623")
                        '("password" . "19880623")
                        '("version" . "608")
                        '("app_name" . "radio_android")
                        '("from" . "android_608_Google")
                        '("client" . "s:mobile|y:android 4.1.1|f:608|m:Google|d:-1178839463|e:google_galaxy_nexus")))
   (qjdb-split-http-header (buffer-string))))


(defun qjdb-parse-channels-json (json-string)
  (qjdb-parse-list-json json-string 'channels
                        (lambda (item)
                          (cons (cdr (assoc 'channel_id item))
                                (cdr (assoc 'name item))))))

(defun qjdb-get-channels-from-web ()
  (qjdb-parse-channels-json
   (with-current-buffer
       (douban-music-send-url douban-music-channels-url)
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
       (douban-music-send-url
        (format douban-music-get-song-list-url channel-number))
     (qjdb-split-http-header (buffer-string)))))

(defun qjdb-set-songs (channel-number)
  (progn
    (setq douban-music-songs
          (qjdb-get-songs-from-web channel-number))
    (setq douban-music-current-song 0)))


(defun douban-music-send-url
  (url &optional url-args callback callback-args)
  "Fetch data from douban music server."
  (let ((url-request-method "GET"))
    (if url-args
        (setq url-request-data
              (mapconcat #'(lambda (arg)
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
;;(qjdb-pause-or-play-song)
;;(qjdb-stop-song)
(defun pick-nth-song-url (n)
  (cdr (assoc 'url (nth n douban-music-songs))))

(defun qjdb-set-current-channel (n)
  (if (not (assoc n douban-music-channels))
      (setq douban-music-current-channel n)))

(defun qjdb-next-song ()
  (interactive)
  (let ((song-url (pick-nth-song-url (+ 1 douban-music-current-song))))
    (if (not song-url)
        (progn
          (qjdb-set-songs douban-music-current-channel)
          (qjdb-next-song))
      (progn
        (qjdb-play-song song-url)
        (setq douban-music-current-song
              (+ 1 douban-music-current-song))))
    (update-qjdb-mode-line-string)))

(defun qjdb-current-song-info ()
  (nth douban-music-current-song douban-music-songs))
(qjdb-current-song-info)

(defun qjdb-current-song-info ()
  (nth douban-music-current-song douban-music-songs))
(defun qjdb-current-song-title()
  (assoc 'title (qjdb-current-song-info)))
(defun qjdb-current-song-artist()
  (assoc 'artist (qjdb-current-song-info)))


(defun update-qjdb-mode-line-string ()
  (setq qjdb-mode-line-string
        (format "%s-%s"
           (cdr (qjdb-current-song-artist))
           (cdr (qjdb-current-song-title))))
  (force-mode-line-update))

(defun qjdb-jump-song ()
  (interactive)
  (progn
    (qjdb-set-songs douban-music-current-channel)
    (qjdb-next-song)))

;;(qjdb-set-songs 1)
;;(setq douban-music-current-song 1)
;;(douban-music-songs)

;; Add the hook to play the next song after current song finished. 
(add-hook 'emms-player-finished-hook
          'qjdb-next-song
          )

(qjdb-set-channels)
(qjdb-next-song)
(qjdb-jump-song)
;; solve problem "Variable binding depth exceeds max-specpdl-size",
;; default value is 1080
(setq max-specpdl-size 34000)
(setq max-lisp-eval-depth 20000)
;;TODO
(defun qjdb-like-song ())
(defun qjdb-ban-song ())
(provide 'qjdb-mode)

(global-mode-string)
;; Mode line setup
(setq-default
 mode-line-format
 '(; Position, including warning for 80 columns
   (:propertize "%4l:" face mode-line-position-face)
   (:eval (propertize "%3c" 'face
                      (if (>= (current-column) 80)
                          'mode-line-80col-face
                        'mode-line-position-face)))
   ; emacsclient [default -- keep?]
   ;;mode-line-client
   " "
   ; read-only or modified status
   (:eval
    (cond (buffer-read-only
           (propertize " RO " 'face 'mode-line-read-only-face))
          ((buffer-modified-p)
           (propertize " ** " 'face 'mode-line-modified-face))
          (t " -- ")))
   qjdb-mode-line-string
   " "
   emms-playing-time-string
   ;; directory and buffer/file name
   (:propertize (:eval (shorten-directory default-directory 30))
                face mode-line-folder-face)
   (:propertize "%b"
                face mode-line-filename-face)
   ; narrow [default -- keep?]
   " %n"
   ; mode indicators: vc, recursive edit, major mode, minor modes, process, global
   (vc-mode vc-mode)
   " "
   (:propertize mode-name
                face mode-line-mode-face)
   " "
   ;;(:eval (propertize (format-mode-line minor-mode-alist)
   ;;'face 'mode-line-minor-mode-face))
   ;;(:propertize mode-line-process
   ;;face mode-line-process-face)
   (global-mode-string global-mode-string)
   ;;   "    "
   ;; nyan-mode uses nyan cat as an alternative to %p
   ;;   (:eval (when nyan-mode (list (nyan-create))))
   ))

;; Helper function
(defun shorten-directory (dir max-length)
  "Show up to `max-length' characters of a directory name `dir'."
  (let ((path (reverse (split-string (abbreviate-file-name dir) "/")))
        (output ""))
    (when (and path (equal "" (car path)))
      (setq path (cdr path)))
    (while (and path (< (length output) (- max-length 4)))
      (setq output (concat (car path) "/" output))
      (setq path (cdr path)))
    (when path
      (setq output (concat ".../" output)))
    output))

;; Extra mode line faces
(make-face 'mode-line-read-only-face)
(make-face 'mode-line-modified-face)
(make-face 'mode-line-folder-face)
(make-face 'mode-line-filename-face)
(make-face 'mode-line-position-face)
(make-face 'mode-line-mode-face)
(make-face 'mode-line-minor-mode-face)
(make-face 'mode-line-process-face)
(make-face 'mode-line-80col-face)

(set-face-attribute 'mode-line nil
    :foreground "gray60" :background "gray20"
    :inverse-video nil
    :box '(:line-width 6 :color "gray20" :style nil))
(set-face-attribute 'mode-line-inactive nil
    :foreground "gray80" :background "gray40"
    :inverse-video nil
    :box '(:line-width 6 :color "gray40" :style nil))

(set-face-attribute 'mode-line-read-only-face nil
    :inherit 'mode-line-face
    :foreground "#4271ae"
    :box '(:line-width 2 :color "#4271ae"))
(set-face-attribute 'mode-line-modified-face nil
    :inherit 'mode-line-face
    :foreground "#c82829"
    :background "#ffffff"
    :box '(:line-width 2 :color "#c82829"))
(set-face-attribute 'mode-line-folder-face nil
    :inherit 'mode-line-face
    :foreground "gray60")
(set-face-attribute 'mode-line-filename-face nil
    :inherit 'mode-line-face
    :foreground "#eab700"
    :weight 'bold)
(set-face-attribute 'mode-line-position-face nil
    :inherit 'mode-line-face
    :family "Menlo" :height 100)
(set-face-attribute 'mode-line-mode-face nil
    :inherit 'mode-line-face
    :foreground "gray80")
(set-face-attribute 'mode-line-minor-mode-face nil
    :inherit 'mode-line-mode-face
    :foreground "gray40"
    :height 110
    )
(set-face-attribute 'mode-line-process-face nil
    :inherit 'mode-line-face
    :foreground "#718c00")
(set-face-attribute 'mode-line-80col-face nil
    :inherit 'mode-line-position-face
    :foreground "black"
    :background "#eab700"
    :background "red")
