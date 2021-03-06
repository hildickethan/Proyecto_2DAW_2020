# -*- coding: utf-8 -*-

from odoo import api, fields, models

class User(models.Model):
    _inherit = 'apirest.base'
    _name = 'classapp.user'
    _description = 'Base user'

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)
    password = fields.Char(string="Password", required=True)

class Admin(models.Model):
    _inherit = 'classapp.user'
    _name = 'classapp.admin'
    _description = 'Admin user'

    teacher_ids = fields.One2many("classapp.teacher", "admin_id", string="Created teachers")

class Teacher(models.Model):
    _inherit = 'classapp.user'
    _name = 'classapp.teacher'
    _description = 'Teacher user'

    admin_id = fields.Many2one("classapp.admin", string="Created by", required=True)
    student_ids = fields.One2many("classapp.student", "teacher_id", string="Students")
    class_ids = fields.One2many("classapp.class", "teacher_id", string="Classes")
    group_ids = fields.One2many("classapp.group", "teacher_id", string="Groups created")

class Student(models.Model):
    _inherit = 'classapp.user'
    _name = 'classapp.student'
    _description = 'Student user'

    currency = fields.Integer(string="Currency", required=True, default="0")
    energy = fields.Integer(string="Energy", required=True, default="100")
    growth = fields.Integer(string="Growth", required=True, default="0")

    teacher_id = fields.Many2one("classapp.teacher", string="Invited by", required=True)
    class_ids = fields.Many2many("classapp.class", string="Classes", required=True)
    skill_ids = fields.Many2many("classapp.skill", string="Available skills")
    cosmetic_ids = fields.Many2many("classapp.cosmetic", string="Purchased cosmetics")
    group_id = fields.Many2one("classapp.group", string="Current group")

# when a teacher clicks to invite emails from frontend
# it sends a request to backend to send it, but we need an Odoo model to send emails correctly
# we create a secondary model to fill in emails to send to the users
# those emails will send them to a register page where they will register as a student and enroll in a class
class Email(models.Model):
    _name = 'classapp.email'
    _description = 'Email model to use to send invitation emails'

    name = fields.Char(string="Email", required=True)

    @api.multi
    def mail_register(self, invite_link):
        template_id = self.env.ref("classapp.student_register_email_template").id
        template = self.env["mail.template"].sudo().browse(template_id)
        template["body_html"] = template["body_html"].replace("[link]", invite_link)
        template.send_mail(self.id, force_send=True)
        template["body_html"] = template["body_html"].replace(invite_link, "[link]")

class Skill(models.Model):
    _inherit = 'apirest.base'
    _name = 'classapp.skill'
    _description = 'Skill model'

    name = fields.Char(string="Name", required=True)
    effect_energy = fields.Integer(string="Effect on energy", required=True)
    effect_growth = fields.Integer(string="Effect on growth", required=True)
    student_ids = fields.Many2many("classapp.student", string="Students with this skill")

class Cosmetic(models.Model):
    _inherit = 'apirest.base'
    _name = 'classapp.cosmetic'
    _description = 'Cosmetic model'

    name = fields.Char(string="Name", required=True)
    image = fields.Char(string="Image URL", required=True)
    student_ids = fields.Many2many("classapp.student", string="Students with this cosmetic")

class Class(models.Model):
    _inherit = 'apirest.base'
    _name = 'classapp.class'
    _description = 'Class model'

    name = fields.Char(string="Name", required=True)
    teacher_id = fields.Many2one("classapp.teacher", string="Class teacher", required=True)
    student_ids = fields.Many2many("classapp.student", string="Class students")
    group_ids = fields.One2many("classapp.group", "class_id", string="Class groups")

class Group(models.Model):
    _inherit = 'apirest.base'
    _name = 'classapp.group'
    _description = 'Group model'

    name = fields.Char(string="Name", required=True)
    class_id = fields.Many2one("classapp.class", string="Class", required=True)
    teacher_id = fields.Many2one("classapp.teacher", string="Created by", required=True)
    student_ids = fields.One2many("classapp.student", "group_id", string="Formed by", required=True)

class RewardPunishment(models.Model):
    _inherit = 'apirest.base'
    _name = 'classapp.rewardpunishment'
    _description = 'Reward and punishment model'

    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description", required=True)
    effect_energy = fields.Integer(string="Effect on energy", required=True)
    effect_growth = fields.Integer(string="Effect on growth", required=True)
    reward_type = fields.Selection(
        string="Type", 
        required=True, 
        selection=[
            ("Reward", "Reward"),
            ("Punishment", "Punishment"),
        ],
    )