# pylint: disable=too-many-lines
import sys
from dataclasses import dataclass, field
import os
import re
from typing import List


# Default ignore list
ignore_directories = [
    ".git",
    ".svn",
    ".mvn",
    ".idea",
    "backup",
    "docs",
    "tests",
    "test",
    "report",
    "reports",
    "node_modules",
    ".terraform",
    ".serverless",
    "venv",
    "examples",
    "tutorials",
    "samples",
    "migrations",
    "db_migrations",
    "unittests",
    "unittests_legacy",
    "stubs",
    "mock",
    "mocks",
]
ignore_files = [
    ".pyc",
    ".gz",
    ".tar",
    ".tar.gz",
    ".tar.xz",
    ".tar",
    ".log",
    ".tmp",
    ".d.ts",
    ".min.js",
    ".min.css",
    ".eslintrc.js",
    ".babelrc.js",
    ".spec.js",
    ".spec.ts",
    ".component.spec.js",
    ".component.spec.ts",
    ".data.js",
    ".data.ts",
    ".bundle.js",
    ".snap",
    ".pb.go",
    ".tests.py",
    ".vdb",
    ".txt",
    ".strings",
    ".nib",
    ".nupkg",
    ".pak",
    ".xml"
]
strings_allowlist = {
    "()",
    "[]",
    "{}",
    " ",
    "&*",
    "(*",
    "$*",
    "!*",
    "*func",
    "*map",
    "Enabled",
    "crypto/",
    "readBase",
    "toFloat",
    "encoding/",
    "*tls",
    "*http",
    "*grpc",
    "protobuf:",
    "*runtime",
    "*x509",
    "*[",
    "*struct",
    "github.com",
    "vendor/",
    "golang.org",
    "gopkg.in",
    "*reflect",
    "*base64",
    "*pgtype",
    "*dsa",
    "*log",
    "*sql",
    "*json",
    "*yaml",
    "*xz",
    "*errors",
    "*flag",
    "*object",
    "*ssh",
    "*syntax",
    "*zip",
    "json:",
    "basic_string",
    "std::",
    "vector::",
    "coreclr_",
    "deps_resolver_",
    "deps_json_",
    "NativeExceptionHolder",
    "System.Runtime",
    "Microsoft-",
    "ProfilerEnum",
    "FastSerialization",
    "InlineDiscretionary",
    "src/libraries",
    "ECDHE-ECDSA-AES256-GCM",
    "setsockopt",
    ".jar",
}

# Method names containing common verbs that could be fuzzed
fuzzable_names = [
    "create",
    "delete",
    "update",
    "insert",
    "upsert",
    "post",
    "put",
    "get",
    "index",
    "encrypt",
    "decrypt",
    "load",
    "import",
    "export",
    "encode",
    "decode",
    "obfuscate",
    "store",
    "fuzz",
    "route",
    "search",
    "find",
    "open",
    "send",
    "receive",
    "approve",
    "reject",
    "password",
    "lock",
    "find",
    "allocate",
    "peer",
    "block",
    "socket",
    "database",
    "remote",
    "api",
    "build",
    "transact",
    "engage",
    "quote",
    "unicode",
    "escape",
    "invoke",
    "execute",
    "process",
    "shell",
    "env",
    "valid",
    "saniti",
    "check",
    "audit",
    "follow",
    "link",
]
fuzzable_names += [
    "expect",
    "add",
    "report",
    "compare",
    "base",
    "close",
    "offer",
    "price",
    "approve",
    "increase",
    "become",
    "propose",
    "decline",
    "raise",
    "estimate",
    "call",
    "design",
    "acquire",
    "gain",
    "reach",
    "announce",
    "fill",
    "became",
    "include",
    "decid",
    "disclose",
    "agree",
    "fail",
    "complete",
    "raise",
    "trade",
    "continue",
    "include",
    "believe",
    "receive",
    "schedule",
    "indicate",
    "provide",
    "help",
    "need",
    "cause",
    "drop",
    "show",
    "order",
    "chang",
    "launch",
    "reduce",
    "plan",
    "want",
    "follow",
    "trade",
    "improve",
    "issu",
    "involve",
    "reject",
    "increase",
    "turn",
    "barr",
    "earn",
    "consent",
    "total",
    "acquire",
    "require",
    "prefer",
    "produce",
    "introduce",
    "consider",
    "suspend",
    "prove",
    "open",
    "close",
    "boost",
    "list",
    "prepare",
    "allow",
    "approve",
    "wrote",
    "reduce",
    "advance",
    "describe",
    "produce",
    "operate",
    "surge",
    "jump",
    "provide",
    "mature",
    "stop",
    "work",
    "introduce",
    "relate",
    "improve",
    "seem",
    "force",
    "leave",
    "believe",
    "develop",
    "decline",
    "expire",
    "invest",
    "settle",
    "change",
    "contribute",
    "elaborate",
    "refuse",
    "quote",
    "pass",
    "threaten",
    "cause",
    "violate",
    "soar",
    "eliminate",
    "create",
    "replace",
    "argue",
    "elect",
    "complete",
    "issue",
    "register",
    "pursue",
    "combine",
    "start",
    "cover",
    "eliminate",
    "plunge",
    "contain",
    "manag",
    "suggest",
    "appear",
    "discover",
    "oppose",
    "form",
    "limit",
    "force",
    "disgorge",
    "attribut",
    "studi",
    "resign",
    "settl",
    "retire",
    "move",
    "anticipat",
    "decide",
    "prompt",
    "maintain",
    "rang",
    "focus",
    "climb",
    "adjust",
    "award",
    "carri",
    "identif",
    "confirm",
    "match",
    "conclude",
    "sign",
    "adopt",
    "accept",
    "expand",
    "exercise",
    "finish",
    "finance",
    "charge",
    "realize",
    "remain",
    "express",
    "replace",
    "deliver",
    "dump",
    "import",
    "assume",
    "capture",
    "join",
    "releas",
    "lower",
    "exce",
    "determin",
    "locat",
    "appli",
    "complain",
    "trigger",
    "enter",
    "intend",
    "purchas",
    "blam",
    "learn",
    "renew",
    "view",
    "speculat",
    "choose",
    "respond",
    "encourage",
    "dismiss",
    "realiz",
    "serve",
    "associat",
    "slipp",
    "spark",
    "negotiate",
    "pleas",
    "divid",
    "financ",
    "execute",
    "discuss",
    "hir",
    "reflect",
    "determine",
    "market",
    "warn",
    "qualifi",
    "explain",
    "impose",
    "recognize",
    "indicate",
    "point",
    "collect",
    "benefit",
    "attach",
    "compete",
    "incurr",
    "remove",
    "share",
    "request",
    "permit",
    "remove",
    "revive",
    "predict",
    "couple",
    "play",
    "commit",
    "revive",
    "kill",
    "present",
    "deserve",
    "convict",
    "agree",
    "accommodate",
    "surrender",
    "restore",
    "restructur",
    "fear",
    "represent",
    "fund",
    "involve",
    "redeem",
    "resolve",
    "obtain",
    "employ",
    "promote",
    "impose",
    "insist",
    "contact",
    "print",
    "advertise",
    "damage",
    "exercis",
    "auction",
    "disappoint",
    "subordinat",
    "secure",
    "integrat",
    "perform",
    "stepp",
    "regulat",
    "trail",
    "occurr",
    "expell",
    "amount",
    "back",
    "regard",
    "conclude",
    "dominat",
    "push",
    "rumor",
    "respect",
    "specifi",
    "support",
    "abandon",
    "figure",
    "extend",
    "tender",
    "unveil",
    "expose",
    "industrializ",
    "regulate",
    "contract",
    "lift",
    "welcom",
    "squeez",
    "prolong",
    "record",
    "announce",
    "assert",
    "inch",
    "manufacture",
    "describe",
    "calculate",
    "favor",
    "train",
    "institut",
    "concern",
    "accelerat",
    "solve",
    "store",
    "assembl",
    "link",
    "advertis",
    "kick",
    "scrambl",
    "skyrocket",
    "target",
    "crippl",
    "stress",
    "manufactur",
    "provoke",
    "handle",
    "poll",
    "endors",
    "balk",
    "compensate",
    "terminate",
    "operate",
    "admit",
    "attract",
    "feature",
    "devote",
    "triple",
    "concentrat",
    "plead",
    "inspir",
    "defend",
    "treat",
    "violat",
    "enforce",
    "surfac",
    "concentrate",
    "suffer",
    "advis",
    "interview",
    "gauge",
    "measur",
    "hamper",
    "nominat",
    "assure",
    "merge",
    "achieve",
    "retain",
    "chair",
    "relegat",
    "mount",
    "Ask",
    "compil",
    "Guarante",
    "position",
    "lock",
    "roll",
    "drift",
    "Estimat",
    "persuade",
    "survive",
    "Found",
    "chastis",
    "handl",
    "press",
    "sweeten",
    "allocat",
    "criticiz",
    "place",
    "prais",
    "install",
    "weigh",
    "perceiv",
    "remark",
    "moderat",
    "stat",
    "rush",
    "surpris",
    "collaps",
    "licens",
    "disagree",
    "publiciz",
    "pressure",
    "drive",
    "omitt",
    "assum",
    "switch",
    "define",
    "sound",
    "invent",
    "absorb",
    "found",
    "observ",
    "desir",
    "sustain",
    "welcome",
    "load",
    "engag",
    "drove",
    "pegg",
    "compromise",
    "enact",
    "negotiate",
    "result",
    "prove",
    "examine",
    "connect",
    "subscribe",
    "organi",
    "diminish",
    "purchase",
    "answer",
    "orient",
    "control",
    "Post",
    "succeed",
    "rewrite",
    "nominate",
    "discharge",
    "entrust",
    "range",
    "attempt",
    "recover",
    "maximize",
    "engage",
    "obligat",
    "label",
    "refuse",
    "denounce",
    "seize",
    "halt",
    "transform",
    "contribute",
    "tolerate",
    "cool",
    "overcome",
    "caution",
    "claim",
    "discontinu",
    "select",
    "participate",
    "bolster",
    "devise",
    "doubt",
    "write",
    "exchange",
    "narrow",
    "strike",
    "diagnos",
    "classif",
    "outlaw",
    "ventilat",
    "slide",
    "track",
    "lengthen",
    "ensnarl",
    "oversee",
    "renovat",
    "accumulat",
    "underscore",
    "guarante",
    "shore",
    "evaluat",
    "clutter",
    "refile",
    "expedit",
    "disput",
    "refund",
    "scrapp",
    "complicate",
    "exist",
    "Regard",
    "halve",
    "store",
    "adapt",
    "achiev",
    "resume",
    "assist",
    "incorporat",
    "capp",
    "stake",
    "outpac",
    "burn",
    "clobber",
    "alarm",
    "fatten",
    "amend",
    "book",
    "watch",
    "number",
    "whistle",
    "perpetuate",
    "root",
    "publish",
    "abide",
    "ration",
    "host",
    "assign",
    "designat",
    "survey",
    "espouse",
    "strapp",
    "twinn",
    "authoriz",
    "paint",
    "accru",
    "swapp",
    "obsess",
    "Film",
    "jostle",
    "populat",
    "curl",
    "dream",
    "resonate",
    "glamorize",
    "collaborat",
    "enabl",
    "chopp",
    "celebrate",
    "scatter",
    "prosecute",
    "unleash",
    "Compare",
    "superimpos",
    "nurtur",
    "shake",
    "interrogat",
    "clean",
    "knitt",
    "assemble",
    "voice",
    "monopolize",
    "spott",
    "Confront",
    "underline",
    "prosecut",
    "enhanc",
    "depend",
    "inflat",
    "educat",
    "fad",
    "stabb",
    "resolv",
    "usher",
    "struggl",
    "distinguish",
    "prepare",
    "copi",
    "broke",
    "car",
    "crowd",
    "decri",
    "overus",
    "enrag",
    "expung",
    "crank",
    "touch",
    "replicat",
    "devis",
    "replicate",
    "discontinue",
    "recommend",
    "embroil",
    "defuse",
    "judg",
    "polariz",
    "discourage",
    "regenerate",
    "Rekindl",
    "averag",
    "protect",
    "prohibit",
    "initiat",
    "mail",
    "quipp",
    "advocate",
    "appoint",
    "exhibit",
    "empower",
    "manipulate",
    "specialize",
    "summon",
    "apologize",
    "emerge",
    "phase",
    "fabricate",
    "speculate",
    "buoy",
    "convinc",
    "erode",
    "trac",
    "recede",
    "flood",
    "bill",
    "alienat",
    "portray",
    "recycle",
    "service",
    "Develop",
    "confuse",
    "materialize",
    "convert",
    "equipp",
    "depress",
    "enclos",
    "single",
    "zoom",
    "command",
    "exhaust",
    "yield",
    "talk",
    "excit",
    "overpric",
    "expir",
    "postpon",
    "reschedul",
    "evaporat",
    "rebuff",
    "review",
    "clamp",
    "interest",
    "license",
    "patent",
    "stirr",
    "devot",
    "escalat",
    "clarifi",
    "cross",
    "penetrate",
    "guid",
    "milk",
    "generate",
    "double",
    "compet",
    "borrow",
    "computerize",
    "analyze",
    "cultivat",
    "tailor",
    "delete",
    "experience",
    "troubl",
    "institute",
    "reopen",
    "knock",
    "synchronize",
    "aggravat",
    "anger",
    "annoy",
    "attend",
    "evoke",
    "scrape",
    "state",
    "memorize",
    "muffl",
    "stare",
    "advance",
    "fill",
    "sack",
    "entitl",
    "dress",
    "decorat",
    "unsettl",
    "breathe",
    "tank",
    "escap",
    "declare",
    "measure",
    "infring",
    "establish",
    "lack",
    "spoke",
    "afflict",
    "harp",
    "seduce",
    "remind",
    "reprove",
    "deteriorat",
    "codifi",
    "pull",
    "acknowledge",
    "hop",
    "arriv",
    "discard",
    "click",
    "visit",
    "disapprove",
    "defin",
    "disciplin",
    "Reach",
    "rectifi",
    "screw",
    "block",
    "emigrate",
    "imagine",
    "tighten",
    "reap",
    "ascribe",
    "tout",
    "acced",
    "entice",
    "pick",
    "impress",
    "entic",
    "befuddl",
    "possess",
    "skipp",
    "graduat",
    "engineer",
    "inherit",
    "diversifi",
    "provok",
    "reallocate",
    "stripp",
    "reallocat",
    "broaden",
    "instruct",
    "draft",
    "waive",
    "bounce",
    "repair",
    "propose",
    "alter",
    "correct",
    "promis",
    "impli",
    "emphasiz",
    "predispose",
    "compos",
    "quote",
    "robb",
    "bother",
    "chose",
    "participat",
    "Choose",
    "depriv",
    "override",
    "impede",
    "impair",
    "dubb",
    "propagandize",
    "clipp",
    "transcribe",
    "happen",
    "disseminate",
    "preclude",
    "mention",
    "examine",
    "disagre",
    "prescribe",
    "assure",
    "react",
    "advocat",
    "convince",
    "exud",
    "Annualiz",
    "clash",
    "evolv",
    "enjoy",
    "recruit",
    "intimidate",
    "Provid",
    "predicat",
    "constru",
    "emasculate",
    "ensure",
    "wast",
    "disapprov",
    "invite",
    "ratifi",
    "characteriz",
    "excise",
    "sav",
    "mortgag",
    "reclaim",
    "parch",
    "profit",
    "curtail",
    "strengthen",
    "cushion",
    "materializ",
    "flirt",
    "fold",
    "brighten",
    "restor",
    "headlin",
    "hand",
    "beleaguer",
    "disclose",
    "approach",
    "screen",
    "miss",
    "preapprov",
    "test-drive",
    "retrac",
    "account",
    "vest",
    "heat",
    "exacerbat",
    "telephone",
    "wedd",
    "wait",
    "sneak",
    "head",
    "curb",
    "battle",
    "entrench",
    "facilitate",
    "stack",
    "constitute",
    "despise",
    "frighten",
    "manage",
    "juggle",
    "automat",
    "dislike",
    "spook",
    "orchestrat",
    "mint",
    "chase",
    "practic",
    "arise",
    "evolve",
    "implement",
    "decrease",
    "sacrifice",
    "Eliminate",
    "please",
    "advise",
    "grapple",
    "appropriat",
    "stifle",
    "notice",
    "document",
    "migrate",
    "color",
    "Fund",
    "Concern",
    "spurn",
    "overvalu",
    "recoup",
    "hunt",
    "promise",
    "breath",
    "enable",
    "combine",
    "insur",
    "look",
    "redistribute",
    "field",
    "concede",
    "endorse",
    "justifi",
    "structur",
    "downgrad",
    "generat",
    "arrang",
    "overstat",
    "circulat",
    "midsiz",
    "eclipse",
    "stretch",
    "debate",
    "assess",
    "revers",
    "chill",
    "insert",
    "outnumber",
    "surge",
    "direct",
    "stimulat",
    "tempt",
    "overdone",
    "waive",
    "notch",
    "search",
    "calculat",
    "tackle",
    "spackle",
    "dispos",
    "stay",
    "revis",
    "conduct",
    "rank",
    "blurr",
    "compare",
    "topp",
    "outdistanc",
    "relaunch",
    "repric",
    "guarantee",
    "hail",
    "despis",
    "subsidize",
    "appease",
    "co-found",
    "coordinate",
    "heighten",
    "nullifi",
    "puzzl",
    "challenge",
    "notifi",
    "clear",
    "delist",
    "explore",
    "emerg",
    "singl",
    "sagg",
    "grant",
    "confus",
    "complicat",
    "Continu",
    "ignor",
    "secede",
    "accrue",
    "term",
    "stemm",
    "magnifi",
    "reimburs",
    "arrive",
    "firm",
    "falter",
    "sense",
    "distribut",
    "experienc",
    "customiz",
    "deriv",
    "avert",
    "slat",
    "realestate",
    "reorganiz",
    "plagu",
    "bounc",
    "reaffirm",
    "demobilize",
    "brush",
    "sabotage",
    "assassinat",
    "avenge",
    "pledg",
    "defeat",
    "rigg",
    "subpoena",
    "plant",
    "explod",
    "centraliz",
    "fizzl",
    "restructure",
    "mitigate",
    "reserv",
    "batter",
    "induce",
    "investigate",
    "estimate",
    "question",
    "trimm",
    "detail",
    "travel",
    "plugg",
    "fashion",
    "arrest",
    "Absorb",
    "finaliz",
    "lease",
    "dash",
    "sputter",
    "harvest",
    "gyrate",
    "scrounge",
    "alleviate",
    "slow",
    "deplete",
    "relieve",
    "compress",
    "delay",
    "influence",
    "plummet",
    "exceed",
    "coat",
    "scuttle",
    "share",
]
secrets_regex = {
    "artifactory": [
        re.compile(r'(?:\s|=|:|"|^)AKC[a-zA-Z0-9]{10,}'),
        re.compile(r'(?:\s|=|:|"|^)AP[\dABCDEF][a-zA-Z0-9]{8,}'),
    ],
    "aws": [
        re.compile(r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"),
        re.compile(r"""(?i)aws(.{0,20})?['"][0-9a-zA-Z/+]{40}['"]"""),
        re.compile(
            r"""amzn.mws.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"""
        ),
        re.compile(r"da2-[a-z0-9]{26}"),
        re.compile(r"s3.amazonaws.com"),
        re.compile(r"ec2-[0-9a-z.-_]+.compute(-1)?.amazonaws.com"),
        re.compile(r"[0-9a-z.-_]+.elb.[0-9a-z.-_]+.amazonaws.com"),
        re.compile(r"[0-9a-z.-_]+.rds.amazonaws\\.com"),
        re.compile(r"[0-9a-z.-_]+.cache.amazonaws.com"),
        re.compile(r"[0-9a-z.-_]+.s3-website[0-9a-z.-_]+.amazonaws.com"),
        re.compile(r"[0-9a-z]+.execute-api.[0-9a-z.\-_]+.amazonaws.com"),
    ],
    "github": [
        re.compile(r"""(?i)github.{0,3}(token|api|key).{0,10}?([0-9a-zA-Z]{35,40})""")],
    "slack": [re.compile(r"""xox[baprs]-([0-9a-zA-Z]{10,48})?""")],
    "EC": [re.compile(r"""-----BEGIN EC PRIVATE KEY-----""")],
    "DSA": [re.compile(r"""-----BEGIN DSA PRIVATE KEY-----""")],
    "OPENSSH": [re.compile(r"""-----BEGIN OPENSSH PRIVATE KEY-----""")],
    "RSA": [re.compile(r"""-----BEGIN RSA PRIVATE KEY-----""")],
    "PGP": [re.compile(r"""-----BEGIN PGP PRIVATE KEY-----""")],
    "google": [
        re.compile(r"""AIza[0-9A-Za-z\-_]{35}"""),
        re.compile(r"""[sS][eE][cC][rR][eE][tT].*['"][0-9a-zA-Z]{32,45}['"]"""),
        re.compile(r"""[sS][eE][cC][rR][eE][tT].*['"][0-9a-zA-Z]{32,45}['"]"""),
        re.compile(r"""[0-9]+-[0-9A-Za-z_]{32}.apps.googleusercontent.com"""),
    ],
    "heroku": [
        re.compile(
            r"""(?i)heroku(.{0,20})?['"][0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}['"]"""
        )
    ],
    "mailchimp": [
        re.compile(r"""(?i)(mailchimp|mc)(.{0,20})?['"][0-9a-f]{32}-us[0-9]{1,2}['"]""")
    ],
    "mailgun": [re.compile(r"""(?i)(mailgun|mg)(.{0,20})?['"][0-9a-z]{32}['"]""")],
    "slack_webhook": [
        re.compile(
            r"https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}"
        )
    ],
    "stripe": [re.compile(r"""(?i)stripe(.{0,20})?['"][s|k]k_live_[0-9a-zA-Z]{24}""")],
    "square": [
        re.compile(r"""sq0atp-[0-9A-Za-z\-_]{22}"""),
        re.compile(r"""sq0atp-[0-9A-Za-z\-_]{43}"""),
    ],
    "twilio": [re.compile(r"""(?i)twilio(.{0,20})?['"][0-9a-f]{32}['"]""")],
    "dynatrace": [re.compile(r"""dt0[a-zA-Z][0-9]{2}\.[A-Z0-9]{24}\.[A-Z0-9]{64}""")],
    "url": [
        re.compile(r"""(http(s)?|s3)://"""),
        re.compile(r"""[a-zA-Z]{3,10}://[^/\s:@]{3,20}:[^/\s:@]{3,20}@.{1,100}["'\s]"""),
        re.compile(
            r"(ftp|jdbc:mysql)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]"
        ),
    ],
    "authorization": [
        re.compile(r"(authorization)\s*:\s*(bearer|token|basic)\s+[0-9a-z.\-_]{6,}"),
        re.compile(r"eyJ[A-Za-z0-9_/+-]*\.[A-Za-z0-9._/+-]*"),
    ],
    "email": [re.compile(r"(?<=mailto:)[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9.-]+")],
    "ip": [
        re.compile(
            r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]).){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(:[0-9]+)?$"
        )
    ],
}

SYMBOL_DELIMITER = "~~"


def get_float_from_env(name, default):
    """
    Retrieves a value from an environment variable and converts it to a
    float. If the value cannot be converted to a float, it returns the
    default value provided.

    :param name:
    :param default:
    :return:
    """
    value = os.getenv(name.upper(), default)
    try:
        value = float(value)
    except ValueError:
        value = default
    return value


def get_int_from_env(name, default):
    """
    Retrieves a value from an environment variable and converts it to an
    integer. If the value cannot be converted to an integer, it returns the
    default value provided.

    :param name:
    :param default:
    """
    return int(get_float_from_env(name, default))


@dataclass
class BlintOptions:
    """
    A data class representing the command-line options for the blint tool.

    Attributes:
        deep_mode (bool): Flag indicating whether to perform deep analysis.
        exports_prefix (list): Prefixes to determine exported symbols.
        fuzzy (bool): Flag indicating whether to perform fuzzy analysis.
        no_error (bool): Flag indicating whether to suppress error messages.
        no_reviews (bool): Flag indicating whether to perform symbol reviews.
        reports_dir (str): The path to the reports directory.
        sbom_mode (bool): Flag indicating whether to perform SBOM analysis.
        src_dir_image (list): A list of source directories.
        sbom_output (str): The path to the output file.
        deep_mode (bool): Flag indicating whether to perform deep analysis.
        export_prefixes (list): Prefixes to determine exported symbols.
        src_dir_boms (list): Directory containing pre-build and build sboms.
    """
    deep_mode: bool = False
    exports_prefix: List = field(default_factory=list)
    fuzzy: bool = False
    no_error: bool = False
    no_reviews: bool = False
    reports_dir: str = ""
    sbom_mode: bool = False
    sbom_output: str = ""
    sbom_output_dir: str = ""
    src_dir_boms: List = field(default_factory=list)
    src_dir_image: List = field(default_factory=list)
    stdout_mode: bool = False
    
    def __post_init__(self):
        if not self.src_dir_image and not (self.sbom_mode and self.src_dir_boms):
            self.sources = [os.getcwd()]
        if not self.reports_dir:
            self.reports_dir = os.getcwd()
        if self.sbom_mode:
            if self.stdout_mode:
                self.sbom_output = sys.stdout
            elif not self.sbom_output:
                self.sbom_output = os.path.join(self.reports_dir, "bom-post-build.cdx.json")
                self.sbom_output_dir = os.path.join(self.reports_dir)
            elif os.path.isdir(self.sbom_output):
                self.sbom_output_dir = self.sbom_output
                self.sbom_output = os.path.join(self.sbom_output, "bom-post-build.cdx.json")
            else:
                self.sbom_output_dir = os.path.dirname(self.sbom_output)
        

# PII related symbols
PII_WORDS = (
    "FirstName",
    "LastName",
    "Phone",
    "Manager",
    "City",
    "Location",
    "Gender",
    "Country",
    "Email",
    "Town",
    "County",
    "PostCode",
    "ZipCode",
    "SSN",
    "MobilePhone",
    "Photo",
    "HomePhone",
    "Address",
    "Card",
    "PinCode",
    "OTP",
    "Calendar",
    "AgentStatus",
    "LastLoginTime",
    "BankAccount"
)

# Some symbols to look for in a first-stage payload
FIRST_STAGE_WORDS = (
    "System.ServiceProcess",
    "System.IO.Compression",
    "System.Reflection.Emit",
    "ICryptoTransform",
    "LoadAssembly",
    "GetEncodedData",
    "add_AssemblyResolve",
    "CreateDecryptor",
    "GetExecutingAssembly",
    "GetModules",
    "get_IsFamilyOrAssembly",
    "/proc/%d/cmdline",
    "/proc/%s/exe",
    "/proc/self/exe",
    "/proc/net/route",
    "/etc/resolv.conf",
    "/usr/lib/systemd/systemd",
    "/usr/compress/bin/",
    "/usr/libexec/openssh/sftp-server",
    "/usr/sbin/reboot",
    "/usr/bin/reboot",
    "/usr/sbin/shutdown",
    "/usr/bin/shutdown",
    "/usr/sbin/poweroff",
    "/usr/bin/poweroff",
    "/usr/sbin/halt",
    "/usr/bin/halt",
    "/proc/self/auxv",
    "/sys/kernel/mm/",
    "virtualboxemulunit",
    "virtualboximportunit",
    "virtualboxunit",
    "qvirtualboxglobalsunit",
    "Uvirtualboxdisasm",
    "loaderx86.dll",
    "ZwProtectVirtualMemory",
    "shlwapi.dll",
    "DeleteCriticalSection"
)
