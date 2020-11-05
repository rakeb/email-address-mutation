# from a shadow_email_address=alice.email.mutation.1@gmail.com this function returns
# real_email_address = alice.email.mutation@gmail.com
# before_at = alice.email.mutation
# mutation_id = 1
# domain = gmail.com
import mailparser


def get_real_email_address(shadow_email_address):
    splitted_shadow_address = shadow_email_address.split('@')
    before_shadow_at = splitted_shadow_address[0]
    domain = splitted_shadow_address[1]

    splitted_before_at = before_shadow_at.rsplit('.', 1)
    mutation_id = splitted_before_at[1]
    before_at = splitted_before_at[0]

    real_email_address = before_at + '@' + domain

    return real_email_address, before_at, mutation_id, domain


def get_mail_from_str(str_mail):
    updated_str_mail = str_mail.split("\r\n", 1)[1];
    mail_object = mailparser.parse_from_string(updated_str_mail)
    from_address = mail_object.from_[0][1]
    to_address = mail_object.to[0][1]
    return to_address, from_address, mail_object


if __name__ == '__main__':
    # print(get_real_email_address('alice.email.mutation.1@gmail.com'))
    static_str_mail = ''' * 15 FETCH (UID 27 RFC822.SIZE 4831 BODY[] {4831}
        Delivered-To: alice.email.mutation@gmail.com
        Received: by 2002:a92:c702:0:0:0:0:0 with SMTP id a2csp1240810ilp;
                Sun, 21 Apr 2019 14:55:39 -0700 (PDT)
        X-Received: by 2002:a63:c112:: with SMTP id w18mr15541321pgf.200.1555883739051;
                Sun, 21 Apr 2019 14:55:39 -0700 (PDT)
        ARC-Seal: i=1; a=rsa-sha256; t=1555883739; cv=none;
                d=google.com; s=arc-20160816;
                b=VeRqj41yaOGb+mjY+dI4ZLCtGybouNI+HbUC93eXP05m+dThfe7Y83SgwSUlGghccd
                 hP37PVXi8DT06wfitEFaYZEdNwZ7JFCVVe76K89dnTCb8HyVZ88p81e+H6j4yiUc6TM9
                 5ntD7Kixm6zGH/a4X7CRjZciRXfsu5i+RYgxFrej7iaByAzviBE3XgR9k77VvPqypT7y
                 LXH9db0+Ju3WosYCy8ukbe31HHt/41hz8W2KPXPAa2APMZ1dSYAFcKDRi03xGeC3q9/W
                 FLiCCCnbPalpUcYpJmWj/fKtP0Eq7YFp1bClA4JhhRLdbSjWK0hCy6Y/sWFf6HAMMVKk
                 IvVA==
        ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;
                h=to:subject:message-id:date:from:mime-version:dkim-signature;
                bh=PinJort92qoGOASGKRMmAE7yT0EGK/8aKO6DJ8HWICw=;
                b=NrckMj6q09ljFkBBK4ryicLIH7NVnIG+Q8TqtjGDbuj29F+X2y1d3qZZKrXQqdY7yT
                 VvJ2hK70W/KxnESsgyPliFTeR70GqVNfDmLUkMSC8ZS1fdP3zuynsoYMYYEqD07nuIiT
                 fwJF7bMIkDqIGlb+LTStl0qelLl0n7HY5DTtlHDJ2JQJ934/deBO0QTzTIQ0M3kOFobR
                 k6fHsnS53s3S+13TMFHYhBeRlMafh303PFmHpiL3pjpZyOGnAe0RCv3cMov91sjZ16ok
                 xkmKDwRBQEhO/0KYCiHO1oPsDUiS1bwslMPlFvmSb8j0B24fC9EXwMp53usuxe1ucsFu
                 GKNw==
        ARC-Authentication-Results: i=1; mx.google.com;
               dkim=pass header.i=@gmail.com header.s=20161025 header.b=eyHqKl1n;
               spf=pass (google.com: domain of rakeb.mazharul.1@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=rakeb.mazharul.1@gmail.com;
               dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com
        Return-Path: <rakeb.mazharul.1@gmail.com>
        Received: from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])
                by mx.google.com with SMTPS id m32sor7723698pld.7.2019.04.21.14.55.38
                for <alice.email.mutation@gmail.com>
                (Google Transport Security);
                Sun, 21 Apr 2019 14:55:39 -0700 (PDT)
        Received-SPF: pass (google.com: domain of rakeb.mazharul.1@gmail.com designates 209.85.220.41 as permitted sender) client-ip=209.85.220.41;
        Authentication-Results: mx.google.com;
               dkim=pass header.i=@gmail.com header.s=20161025 header.b=eyHqKl1n;
               spf=pass (google.com: domain of rakeb.mazharul.1@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=rakeb.mazharul.1@gmail.com;
               dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com
        DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
                d=gmail.com; s=20161025;
                h=mime-version:from:date:message-id:subject:to;
                bh=PinJort92qoGOASGKRMmAE7yT0EGK/8aKO6DJ8HWICw=;
                b=eyHqKl1n0P2VoQxH7x4R/jVUo3JLAdc4SWL1L0EBRHGyvQtEfv0ELVwUPEhJs/k0XF
                 vkQVaCTUAN6yO6+5jxLiemereyvjasU3QNz8XpC2kr4aI6ocz/iHwKx00tzOCyc5j8Wh
                 tNnSiA5nz0PCMLOzQf5m/zvBs1KxwE0y7UPlquwu8Za1yOL+F2YDXQ7pxx0yi0AAOkmv
                 CaAS2dF2vn6QaH3EtEWtasL/oSpwAo7leSZ0Db6wOjhbX0oR+c3MLOswjt9O+07ZleH7
                 F8LhetqEeDNvmEmBu3305ohQFc2Kl41nkrs2vGQuLhaWZJ/GI0bx/xB7YXqIM8PCFczu
                 Gu2g==
        X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
                d=1e100.net; s=20161025;
                h=x-gm-message-state:mime-version:from:date:message-id:subject:to;
                bh=PinJort92qoGOASGKRMmAE7yT0EGK/8aKO6DJ8HWICw=;
                b=rtfRge8kXC7RYDlQxfj+Axaho6QxT2h3j3B7f6lcWkqfsRH8yo5uhPgYhG59msoI1l
                 7NSJWjlY+so1xDMC5Q+Kqs9Co5sLK+FTgFA+CWuMH+3dJp+E9YxGv6lzDc7fgwv8u1HY
                 j79ZhUQ3jlveqrH2bKD10gkcKzk0ZWV1p1Ox8GbzDvJ9pPooXFLuykKMfWyvr1Mzeh0F
                 6mQQafCOHdeKHBK7KdgaKkB+9uzf0zqMJa/dnA2x6MPbGrk+1v2HPZac6Gi/v5j9Ro7X
                 jkEqOmUp1M2/pwGCouBZe6jp+wAKGoS8I6hnNZlr3uQotSQQoW+jHrLdTf+Af84kLtgl
                 +jVA==
        X-Gm-Message-State: APjAAAV++SQX/hdDx5QIXtPfVYCV1puQULXToB4Iz4KrSQhKIyfKqB0v
        	IFVimkypE9VFDnZxlGd+jln2+1iV0wjGbymT8SEKIw==
        X-Google-Smtp-Source: APXvYqxFFvPM3DIQxtAJJB8Hj78YrZow1hqnCKtaPgQ2+eWUQeyNYH4+d8yShGUChelwBISz1vUnMA+qY1O3aSPKxvw=
        X-Received: by 2002:a17:902:9a95:: with SMTP id w21mr16933494plp.74.1555883738757;
         Sun, 21 Apr 2019 14:55:38 -0700 (PDT)
        MIME-Version: 1.0
        From: Rakeb Mazharul <rakeb.mazharul.1@gmail.com>
        Date: Sun, 21 Apr 2019 17:55:28 -0400
        Message-ID: <CAAUuxHO=RKqDaFfegm9Be0N+RhQzEM7f+c+FFF_J6pqSrGOYbQ@mail.gmail.com>
        Subject: lets see how it works
        To: alice.email.mutation@gmail.com
        Content-Type: multipart/alternative; boundary="0000000000008f801605871169e0"

        --0000000000008f801605871169e0
        Content-Type: text/plain; charset="UTF-8"

        This may not work correctly.

        --0000000000008f801605871169e0
        Content-Type: text/html; charset="UTF-8"

        <div dir="ltr">This may not work correctly.</div>

        --0000000000008f801605871169e0--
        )
        6 OK Success'''