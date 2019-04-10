$(function() {

    function capitalize(str) {
        return str.toLowerCase()
            .split('-')
            .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
            .join('-')
            .split(' ')
            .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
            .join(' ');
    }

    function translateToEn(str, target = false) {
        let ru = {
                'а': 'a',
                'б': 'b',
                'в': 'v',
                'г': 'g',
                'д': 'd',
                'е': 'e',
                'є': 'ie',
                'ж': 'zh',
                'з': 'z',
                'и': 'y',
                'і': 'i',
                'ї': 'i',
                'к': 'k',
                'л': 'l',
                'м': 'm',
                'н': 'n',
                'о': 'o',
                'п': 'p',
                'р': 'r',
                'с': 's',
                'т': 't',
                'у': 'u',
                'ф': 'f',
                'х': 'kh',
                'ц': 'ts',
                'ч': 'ch',
                'ш': 'sh',
                'щ': 'shch',
                'ы': 'y',
                'э': 'e',
                'ю': 'iu',
                'я': 'ia'
            },
            translited = [];

        if (str.length > 0) {
            str = str.replace(/й/g, 'i').replace(/Й/g, 'Y').replace(/Є/g, 'Ye').replace(/Ї/g, 'Yi').replace(/Ю/g, 'Yu').replace(/Я/g, 'Ya').replace(/[ъь]+/g, '');

            for (let i = 0; i < str.length; ++i) {
                translited.push(
                    ru[ str[i] ]
                    || ru[ str[i].toLowerCase() ] == undefined && str[i]
                    || ru[ str[i].toLowerCase() ].replace(/^(.)/, function ( match ) { return match.toUpperCase() })
                );
            }

            target.val(translited.join(''));
        }
        else {
            target.val('');
        }
    }

    // translit cyrilic to latin
    let isFirstNameEn = false,
        isLastNameEn = false;
    $('#id_last_name_en').on('keyup', function() {
        let node = $(this);
        node.val(node.val().replace(/[^[a-zA-Z\-\'\s]/g, ''));
        node.val(capitalize(node.val()));

        ($(this).val().length > 0)
            ? isLastNameEn = true
            : isLastNameEn = false;
    });

    $('#id_first_name_en').on('keyup', function() {
        let node = $(this);
        node.val(node.val().replace(/[^[a-zA-Z\-\'\s]/g, ''));
        node.val(capitalize(node.val()));

        ($(this).val().length > 0)
            ? isFirstNameEn = true
            : isFirstNameEn = false;
    });

    $('#id_last_name_ukr').on('keyup', function() {
        let node = $(this);
        node.val(node.val().replace(/[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/]/g, ''));
        node.val(capitalize(node.val()));

        if (!isLastNameEn) {
            translateToEn($(this).val(), $('#id_last_name_en'));
        }
    });

    $('#id_first_name_ukr').on('keyup', function() {
        let node = $(this);
        node.val(node.val().replace(/[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/]/g, ''));
        node.val(capitalize(node.val()));

        if (!isFirstNameEn) {
            translateToEn($(this).val(), $('#id_first_name_en'));
        }
    });

    $('#id_second_name_ukr').on('keyup', function() {
        let node = $(this);
        node.val(node.val().replace(/[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/]/g, ''));
        node.val(capitalize(node.val()));
    });
});