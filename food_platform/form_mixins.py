class BootstrapFormMixin:
    base_input_class = "form-control"
    error_input_class = "is-invalid"

    def _apply_bootstrap_field_classes(self):
        """
        Проставляет базовый класс Bootstrap и error-class для валидируемых полей.
        Дает красную рамку через is-invalid после валидации.
        """
        if self.is_bound:
            _ = self.errors

        for name, field in self.fields.items():
            attrs = field.widget.attrs
            classes = attrs.get("class", "").split()

            if self.base_input_class and self.base_input_class not in classes:
                classes.append(self.base_input_class)

            if self.is_bound and self.errors.get(name):
                if self.error_input_class not in classes:
                    classes.append(self.error_input_class)

            attrs["class"] = " ".join(filter(None, classes))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_field_classes()

    def is_valid(self):
        is_valid = super().is_valid()
        self._apply_bootstrap_field_classes()
        return is_valid

