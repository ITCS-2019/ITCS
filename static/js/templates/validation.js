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

    $('input', '.date').attr('autocomplete', 'off');

    // allow only latin letters, space, hyphen, apostrophe
    function enLettersValid(node) {
        node.val(node.val().replace(/[^[a-zA-Z\-\'\s]/g, ''));
        node.val(capitalize(node.val()));
    }

    // allow only cyrilic letters, space, hyphen, apostrophe
    function cyrLettersValid(node) {
        node.val(node.val().replace(/[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/]/g, ''));
        node.val(capitalize(node.val()));
    }

    // allow only numbers and hyphen
    function numbersValid(node) {
        node.val(node.val().replace(/[^0-9-]/g, ''));
    }

    // allow cyrilic/latin letters, space, hyphen, apostrophe
    function allLettersValid(node) {
        node.val(node.val().replace(/[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/a-zA-Z/"/]/g, ''));
    }

    // Deny cyrilic letters
    function denyCyrilic(node) {
        node.val(node.val().replace(/[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ /'//"/]/g, ''));
    }

    // translit cyrilic to latin
    let isFirstNameEn = false,
        isLastNameEn = false;
    $('#id_last_name_en').on('keyup', function() {
        enLettersValid($(this));

        ($(this).val().length > 0)
            ? isLastNameEn = true
            : isLastNameEn = false;
    });

    $('#id_first_name_en').on('keyup', function() {
        enLettersValid($(this));

        ($(this).val().length > 0)
            ? isFirstNameEn = true
            : isFirstNameEn = false;
    });

    $('#id_last_name_ukr').on('keyup', function() {
        cyrLettersValid($(this));

        if (!isLastNameEn) {
            translateToEn($(this).val(), $('#id_last_name_en'));
        }
    });

    $('#id_first_name_ukr').on('keyup', function() {
        cyrLettersValid($(this));

        if (!isFirstNameEn) {
            translateToEn($(this).val(), $('#id_first_name_en'));
        }
    });

    $('#id_second_name_ukr').on('keyup', function() {
        cyrLettersValid($(this));
    });

    $('#id_form_number').on('keyup', function() {
        numbersValid($(this));
    });

    $('#id_certf_number').on('keyup', function() {
        numbersValid($(this));
    });

    // Add/Edit training organization form
    $('#id_organisation_id').on('keyup', function() {
        numbersValid($(this));
    });

    $('#id_organisation_name').on('keyup', function() {
        allLettersValid($(this));
    });

    $('#id_orgnisation_email').on('keyup', function() {
        denyCyrilic($(this));
    });

    // Range numbers
    $('#id_rangeStart').on('keyup', function() {
        numbersValid($(this));
        if (~~$(this).val() >= ~~$('#id_rangeEnd').val()
        && $('#id_rangeEnd').val().length > 0) {
            $(this).val($(this).val().slice(0, -1));
        }
    });

    $('#id_rangeEnd').on('keyup', function() {
        numbersValid($(this));
    });

    $('#id_rangeEnd').on('blur', function() {
        if (~~$(this).val() <= ~~$('#id_rangeStart').val()) {
            $(this).val('');
        }
    });
});